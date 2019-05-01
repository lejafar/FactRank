import pathlib

import torch
import torch.nn.functional as F
from sklearn.metrics import confusion_matrix

from factrank.model import CNNText
from factrank.util.processing import create_fields, create_dataset

def main():

    statement_field, label_field = create_fields()
    train_iterator, test_iterator = create_dataset('data/sentence_dump_1.0_28.04.2019.csv', statement_field, label_field, batch_size=128)

    # create model
    embed_num = len(statement_field.vocab)
    class_num = len(label_field.vocab)
    print(f"class_num: {class_num}")
    class_weight = torch.tensor([1 / count for count in sorted(label_field.vocab.freqs.values(), reverse=True)])
    print(f"class frequencies: {label_field.vocab.freqs}")
    print(f"class_weight: {class_weight}")
    cnn = CNNText(embed_num, class_num, dropout=.9, static=False)

    train(train_iterator, test_iterator, cnn, class_weight=class_weight)

def train(train_iterator, test_iterator, model, lr=0.001, max_epochs=300, class_weight=None):

    if torch.cuda.is_available():
        model.cuda()

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    steps = best_acc = last_step = 0
    for epoch in range(1, max_epochs+1):

        model.train()
        for step, train_batch in enumerate(train_iterator):
            feature, target = train_batch.statement.transpose(0, 1), train_batch.label

            target_factual = (target != 0).float()

            if torch.cuda.is_available():
                feature, target = feature.cuda(), target.cuda()

            optimizer.zero_grad()

            logit = model(feature)
            logit_factual = model.factual

            loss = F.cross_entropy(logit, target, weight=class_weight)
            loss_factual = F.binary_cross_entropy_with_logits(logit_factual.squeeze(), target_factual)

            #loss = loss_factual # + loss

            loss.backward()
            optimizer.step()

            if step % 10 == 0:
                correct = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
                accuracy = 100.0 * correct / train_batch.batch_size
                print(f"Epoch[{epoch}] Batch[{step}] - loss: {loss.item():.6f} acc: {accuracy:.4f}% ({correct} / {train_batch.batch_size})")
                #correct_factual = ((F.sigmoid(logit_factual) > 0.5).float().view(target_factual.size()).data == target_factual.data).sum()
                #accuracy_factual = 100.0 * correct_factual / train_batch.batch_size
                #print(f"Epoch[{epoch}] Batch[{step}] - loss_factual: {loss_factual.item():.6f} acc: {accuracy_factual:.4f}% ({correct_factual} / {train_batch.batch_size})")

        test_acc = evaluate(test_iterator, model, class_weight)
        if test_acc > best_acc:
            best_acc = test_acc
            last_step = step
            save_model(model, 'checkpoints', 'best', round(test_acc.item()))

def evaluate(iterator, model, class_weight):

    model.eval()
    correct, avg_loss = 0, 0
    for batch in iterator:
        feature, target = batch.statement.transpose(0, 1), batch.label

        target_factual = (target != 0).float()

        if torch.cuda.is_available():
            feature, target = feature.cuda(), target.cuda()

        logit = model(feature)
        logit_factual = model.factual

        loss = F.cross_entropy(logit, target, weight=class_weight)
        loss_factual = F.binary_cross_entropy_with_logits(logit_factual.squeeze(), target_factual)

        #loss = loss_factual # + loss

        avg_loss += loss.item()

        correct += (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
        print(confusion_matrix(target.data.numpy(), torch.max(logit, 1)[1].numpy()))
        #correct_factual = ((F.sigmoid(logit_factual) > 0.5).float().view(target_factual.size()).data == target_factual.data).sum()
        #print(confusion_matrix(target_factual.data.numpy(), (F.sigmoid(logit_factual) > .5).numpy()))

    size = len(iterator.dataset)
    avg_loss /= size
    accuracy = 100.0 * correct / size
    print(f"Evaluation - loss: {avg_loss:.6f}  acc: {accuracy:.4f}% ({correct}/{size})")
    #accuracy_factual = 100.0 * correct_factual / size
    #print(f"Evaluation - loss_factual: {avg_loss:.6f}  acc: {accuracy_factual:.4f}% ({correct_factual}/{size})")

    return accuracy

def save_model(model, folder, prefix="", step=""):
    folder = pathlib.Path(folder)
    folder.mkdir(exist_ok=True, parents=True)
    torch.save(model.state_dict(), folder / f"{prefix}_model_{step}.pth")

if __name__ == "__main__":
    main()
