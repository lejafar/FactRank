import logging
import pathlib

import pandas as pd
import torch
from descriptors import cachedproperty

from .tokenize import Tokenize
from .log import log_runtime

from torch.utils.data import TensorDataset

logger = logging.getLogger(__name__)


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


class BertStatementProcessor:
    """ processes text or sentences into tensor of indices meaningfull to the Bert based network """

    def __init__(self, options):
        self.options = options

    def encode(self, sentence):
        inputs = self.tokenizer.encode_plus(sentence,
                                            None,
                                            add_special_tokens=True,
                                            return_tensors='pt',
                                            truncation=True)
        return inputs["input_ids"], inputs["token_type_ids"]

    @cachedproperty
    def tokenizer(self):
        from transformers import BertTokenizer
        return BertTokenizer.from_pretrained(self.options.pretrained_model_shortcut)

    @cachedproperty
    def sentencize(self):
        return Tokenize().sentencize

    @property
    def label_list(self):
        return ["FR", "FNR", "NF"]

    @property
    def label_map(self):
        return {label: i for i, label in enumerate(self.label_list)}


class BertDataProcessor:

    def __init__(self, options, statement_processor, csv_path):
        self.options = options
        self.statement_processor = statement_processor
        self.csv_path = csv_path

    @property
    def tokenizer(self):
        return self.statement_processor.tokenizer

    @cachedproperty
    @log_runtime("reading in DataFrame")
    def dataframe(self):
        full_path = pathlib.Path(__file__).parent / self.csv_path
        logger.info("loading %s", full_path)
        return pd.read_csv(full_path)

    @cachedproperty
    @log_runtime("creating features")
    def features(self):
        from transformers import InputFeatures
        # load features
        features = []
        for i, (_, statement, label) in enumerate(self.dataframe.itertuples(index=False)):
            inputs = self.tokenizer.encode_plus(statement,
                                                None,
                                                add_special_tokens=True,
                                                max_length=self.options.max_seq_length)
            input_ids, token_type_ids = inputs["input_ids"], inputs["token_type_ids"]

            # The mask has 1 for real tokens and 0 for padding tokens, so only real tokens are attended to
            attention_mask = [1] * len(input_ids)

            # apply zero-padding up to the sequence length
            padding_length = self.options.max_seq_length - len(input_ids)
            pad_token = self.tokenizer.convert_tokens_to_ids([self.tokenizer.pad_token])[0]
            input_ids = input_ids + ([pad_token] * padding_length)
            attention_mask = attention_mask + ([0] * padding_length)
            token_type_ids = token_type_ids + ([0] * padding_length)

            # check consistency
            assert len(input_ids) == self.options.max_seq_length
            assert len(attention_mask) == self.options.max_seq_length
            assert len(token_type_ids) == self.options.max_seq_length

            label_id = self.statement_processor.label_map[label]

            if i % 1000 == 0:
                logger.info("*** example feature %s ***" % i)
                logger.info("statement: %s" % statement)
                logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
                logger.info("attention_mask: %s" % " ".join([str(x) for x in attention_mask]))
                logger.info("token_type_ids: %s" % " ".join([str(x) for x in token_type_ids]))
                logger.info("label: %s (id = %d)" % (label, label_id))

            features.append(
                InputFeatures(input_ids=input_ids,
                              attention_mask=attention_mask,
                              token_type_ids=token_type_ids,
                              label=label_id))
        return features

    @property
    def dataset(self):
        """ create DataSet from list of InputFeatures """

        all_input_ids = torch.tensor([f.input_ids for f in self.features], dtype=torch.long)
        all_attention_mask = torch.tensor([f.attention_mask for f in self.features], dtype=torch.long)
        all_token_type_ids = torch.tensor([f.token_type_ids for f in self.features], dtype=torch.long)
        all_labels = torch.tensor([f.label for f in self.features], dtype=torch.long)

        return TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids, all_labels)
