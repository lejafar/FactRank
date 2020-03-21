import pathlib
import logging
from dataclasses import replace

from descriptors import cachedproperty
from torchtext import data
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix

from .factnet import FactNet
from .options import Options
from .log import init_package_logger

l = logging.getLogger(__name__)

class Evaluator:

    def __init__(self, model_name, statements_eval_path='data/training/statements_val.csv'):
        self.model_name = model_name
        self._statements_eval_path = statements_eval_path

    @property
    def statements_eval_path(self):
        return pathlib.Path(__file__).parent / 'data/training/statements_val.csv'

    @cachedproperty
    def factnet(self):
        run_path = pathlib.Path(__file__).parent / f'../log/{self.model_name}'
        options = replace(Options.load(run_path / 'factnet.options.yml'), gpu_id=2)
        init_package_logger(options)
        return FactNet(options)

    @cachedproperty
    def model(self):
        return self.factnet.model

    @cachedproperty
    def dataset(self):
        data_fields = [('id', None), ('statement', self.factnet.statement_field), ('label', self.factnet.label_field)]
        return data.TabularDataset(self.statements_eval_path, format='csv', fields=data_fields, skip_header=True)

    @cachedproperty
    def dataloader(self):
        return data.Iterator(self.dataset, batch_size=50)

    def evaluate(self, gpu_id=2):

        self.model.eval()
        correct, avg_loss = 0, 0
        for batch in self.dataloader:

            feature, target = batch.statement.transpose(0, 1), batch.label
            feature, target = feature.to(gpu_id), target.to(gpu_id)

            logit = self.model(feature)

            correct += (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
            l.info(confusion_matrix(target.data.cpu().numpy(), torch.max(logit, 1)[1].cpu().numpy()))

        size = len(self.dataset)
        avg_loss /= size
        accuracy = 100.0 * correct / size

        print(f"Evaluation - acc: {accuracy:.4f}% ({correct}/{size})")

if __name__ == "__main__":
    Evaluator(model_name="test_10").evaluate()
