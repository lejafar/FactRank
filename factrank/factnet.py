import logging
import pathlib

from descriptors import cachedproperty
from torchtext import data
import torch
import torch.nn.functional as F
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np

from .modules import CNNText
from .processing import FieldProcessor, StatementProcessor
from .tokenize import Tokenize

l = logging.getLogger(__name__)

class FactNet:

    def __init__(self, options=None):
        self.options = options

        self._statement_field = data.Field(lower=True, tokenize=Tokenize(self.options).tokenize)
        self._label_field = data.Field(sequential=False, unk_token=None)

    @property
    def model_path(self):
        return self.options.run_path / f"{self.options.prefix}.cnn.pth"

    @cachedproperty
    def model(self):
        """ create new model or load pre-trained if available """

        embed_num = len(self.statement_field.vocab)
        class_num = len(self.label_field.vocab)
        cnn = CNNText(embed_num, class_num, self.options)

        if self.model_path.exists():
            # we have a pre-trained model in run_path so we'll load this
            l.info("loading pre-trained model from %s", self.model_path)
            cnn.load_state_dict(torch.load(self.model_path, map_location=self.options.gpu_id))
            cnn.eval() # switch model to 'eval' mode, turning off dropout and batch_norm
            return cnn

        if self.pre_trained_word_embeddings is not None:
            cnn.set_pre_trained_word_embeddings(self.pre_trained_word_embeddings)

        return cnn

    def save(self):
        self.model_path.parent.mkdir(exist_ok=True, parents=True)
        l.info("saving model to %s", self.model_path)
        torch.save(self.model.state_dict(), self.model_path)

    @property
    def statement_field(self):
        return self.statement_processor.field

    @cachedproperty
    def statement_processor(self):
        """ processes text into tensor of indices meaningfull to the network """
        return self.get_processor("statement", StatementProcessor, self._statement_field)

    @property
    def label_field(self):
        return self.label_processor.field

    @cachedproperty
    def label_processor(self):
        return self.get_processor("label", FieldProcessor, self._label_field)

    def get_processor(self, name, cls, field):
        """ a processor of a field handles either restoring or building vocabulary & saving for inference """

        processor_path = self.options.run_path / f"{self.options.prefix}.{name}-processor.pth"
        if processor_path.exists():
            # we have a pre-build processor in run_path so we'll load this
            l.info("loading %s-processor from %s", name, processor_path)
            return cls(self.options).load(processor_path)
        else:
            # we create a new processor and build it's vocabulary based on the training set
            train, test = self.datasets
            processor = cls(self.options, field).build_vocab(train)
            l.info("saving %s-processor to %s", name, processor_path)
            processor.save(processor_path)
            return processor

    @cachedproperty
    def datasets(self):
        data_fields = [('id', None), ('statement', self._statement_field), ('label', self._label_field)]

        statements_train_path = pathlib.Path(__file__).parent / self.options.statements_train_path
        # load statements purely for logging label counts
        l.info("loading training statements from %s", statements_train_path)
        statements_train = pd.read_csv(statements_train_path)
        l.info(statements_train.groupby('label').count())
        train = data.TabularDataset(statements_train_path, format='csv', fields=data_fields, skip_header=True)

        statements_test_path = pathlib.Path(__file__).parent / self.options.statements_test_path
        # load statements purely for logging label counts
        l.info("loading test statements from %s", statements_test_path)
        statements_test = pd.read_csv(statements_test_path)
        l.info(statements_test.groupby('label').count())
        test = data.TabularDataset(statements_test_path, format='csv', fields=data_fields, skip_header=True)

        return train, test

    @cachedproperty
    def dataloaders(self):
        train_set, test_set = self.datasets
        train, test = data.Iterator.splits((train_set, test_set),
                                           batch_sizes=(self.options.batch_size, len(test_set)),
                                           device=self.options.gpu_id,
                                           repeat=False,
                                           sort_key=lambda x: (len(x.statement)),
                                           shuffle=True)
        return train, test

    @cachedproperty
    def pre_trained_word_embeddings(self):

        embeddings_path = pathlib.Path(__file__).parent / self.options.word_embeddings_path
        if embeddings_path.exists():
            # we'll create a tensor consisting of the pre-trained
            # embeddings in the order they occur in the vocabulary
            l.info("loading pre-trained word embeddings from %s", embeddings_path)
            import gensim.models # don't want to make this a dependency
            embeddings = gensim.models.KeyedVectors.load_word2vec_format(embeddings_path, binary=False)

            in_voc = 0
            pre_trained_word_embeddings = []
            #with open(embeddings_path.parent / 'cow-big-slim.txt', 'w') as f:
            for word in self.statement_field.vocab.stoi:
                if word in embeddings:
                    in_voc += 1
                    #f.write(word + " " + " ".join([str(el) for el in embeddings[word]]) + "\n")
                    pre_trained_word_embeddings.append(embeddings[word])
                else:
                    # initial out-of-vocabulary vectors with zero vector
                    pre_trained_word_embeddings.append(np.zeros(embeddings.vector_size).astype(np.float32))

            pre_trained_word_embeddings = np.stack(pre_trained_word_embeddings)
            l.info(f"{in_voc / len(pre_trained_word_embeddings) * 100:.4f} % in vocabulary of length {len(pre_trained_word_embeddings)}")
            return torch.from_numpy(pre_trained_word_embeddings.astype(np.float32))


    def fit(self):
        """ train network """

        train_loader, _ = self.dataloaders
        steps = best_accuracy = 0
        for epoch in range(self.options.max_epochs):

            self.model.train()

            for step, train_batch in enumerate(train_loader):

                feature, target = train_batch.statement.transpose(0, 1), train_batch.label
                feature, target = feature.to(self.options.gpu_id), target.to(self.options.gpu_id)

                self.model.optimizer.zero_grad()

                logit = self.model(feature)
                loss = F.cross_entropy(logit, target)

                loss.backward()
                self.model.optimizer.step()

                if step % self.options.log_metrics_step == 0:
                    correct = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
                    accuracy = 100.0 * correct / train_batch.batch_size
                    learning_rate = [param_group['lr'] for param_group in self.model.optimizer.param_groups][0]
                    l.info(f"Epoch[{epoch}] Batch[{step}] - loss: {loss.item():.6f} acc: {accuracy:.4f}% ({correct} / {train_batch.batch_size}) lr: {learning_rate:.4f}")

            self.model.schedule.step()

            if epoch % self.options.log_metrics_step == 0:
                test_accuracy = self.evaluate()
                if test_accuracy > best_accuracy:
                    best_accuracy = test_accuracy
                    self.save()

                l.info(f"Epoch[{epoch}] - best model so far {best_accuracy:.4f}")

    def evaluate(self):
        _, test_loader = self.dataloaders

        self.model.eval()
        correct, avg_loss = 0, 0
        for test_batch in test_loader:

            feature, target = test_batch.statement.transpose(0, 1), test_batch.label
            feature, target = feature.to(self.options.gpu_id), target.to(self.options.gpu_id)

            logit = self.model(feature)
            loss = F.cross_entropy(logit, target)

            avg_loss += loss.item()

            correct += (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
            l.info(confusion_matrix(target.data.cpu().numpy(), torch.max(logit, 1)[1].cpu().numpy()))

        size = len(test_loader.dataset)
        avg_loss /= size
        accuracy = 100.0 * correct / size

        l.info(f"Evaluation - loss: {avg_loss:.6f}  acc: {accuracy:.4f}% ({correct}/{size})")

        return accuracy

    def infer(self, text_or_sentences):
        if isinstance(text_or_sentences, str):
            # it's not yet list of sentences so we'll split the text
            text_or_sentences = self.statement_processor.sentencize(text_or_sentences)
        return self(text_or_sentences)

    def __call__(self, sentences, batch_size=1):
        """ infer label for all sentences """
        # translate sentences to tensor of indices meaningfull to the model
        feature = self.statement_processor(sentences)
        feature = feature.transpose(0, 1)

        # compute logits
        self.model.eval() # make sure it's set to evaluate
        logits = []
        for i in range(max(1, len(feature) // batch_size)):
            logits.append(self.model(feature[i * batch_size:(i+1) * batch_size]))
        logit = torch.stack(logits, dim=1).squeeze(0)
        #logit = self.model(feature)

        # translate logits in labels & probabilities
        probs = F.softmax(logit, dim=1)
        max_args = torch.argmax(probs, dim=-1)
        max_probs, _ = torch.max(probs, dim=-1)

        for sentence, max_arg, max_prob, prob in zip(sentences, max_args, max_probs, probs):
            all_probs = {self.label_processor[dim]: p.item() for dim, p in enumerate(prob)}
            yield self.label_processor[max_arg], max_prob.item(), all_probs, sentence

    def checkworthyness(self, text_or_sentences):
        return sorted([(all_probs['FR'], sentence) for *_, all_probs, sentence in self.infer(text_or_sentences)], reverse=True)
