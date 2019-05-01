import csv
import os

from torchtext import data
import pandas as pd

from .tokenize import Tokenize

def create_fields():

    t_statement = Tokenize()

    statement = data.Field(lower=True, tokenize=t_statement.tokenizer)
    label = data.Field(sequential=False, unk_token=None)

    return statement, label

def create_dataset(statements_csv_path, statement_field, label_field, min_strlen=5, max_strlen=50, batch_size=32, device=-1):

    statements = pd.read_csv(statements_csv_path)
    statements = statements[statements.label != "ERR"]
    statements.pop("id")

    # filter out statements that are too short or too long
    mask = (statements.statement.str.count(' ') < max_strlen) & (statements.statement.str.count(' ') > min_strlen)
    statements= statements.loc[mask]

    statements.to_csv("statements_tmp.csv", index=False)
    data_fields = [('statement', statement_field), ('label', label_field)]
    dataset = data.TabularDataset('statements_tmp.csv', format='csv', fields=data_fields, skip_header=True)
    os.remove('statements_tmp.csv') # clean up tmp file

    train, test = dataset.split(split_ratio=0.8, stratified=True, strata_field='label')

    # create vocabulary
    statement_field.build_vocab(train, test, min_freq=3)
    label_field.build_vocab(train, test)

    train_iterator, test_iterator = data.Iterator.splits((train, test), batch_sizes=(batch_size, len(test)),
            device=device, repeat=False, sort_key=lambda x: (len(x.statement)), shuffle=True)

    return train_iterator, test_iterator

