import torch

from .tokenize import Tokenize

class FieldProcessor:
    """ processes fields """

    def __init__(self, options, field=None):
        self.options = options
        self.field = field

    def load(self, path):
        " load pre-build field "
        with open(path, 'rb') as f:
            self.field = torch.load(f)
            return self

    def save(self, path):
        " save pre-build field "
        with open(path, 'wb') as f:
            torch.save(self.field, f)

    def __getitem__(self, index):
        """ index to str """
        return self.field.vocab.itos[index]

    def build_vocab(self, *datasets):
        self.field.build_vocab(*datasets)
        return self

class StatementProcessor(FieldProcessor):
    """ processes text or sentences into tensor of indices meaningfull to the network """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokenizer = Tokenize()

    def build_vocab(self, *datasets):
        self.field.build_vocab(*datasets, min_freq=self.options.min_freq)
        return self

    def __call__(self, sentences):
        """ transforms sentences into something that is meaningfull to the network """
        tokenized = [self.tokenizer.tokenize(sentence) for sentence in sentences]
        return self.field.process(tokenized)

    def sentencize(self, text):
        """ splits text into sentences """
        return list(self.tokenizer.sentencize(text))
