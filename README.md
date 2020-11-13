# FactRank

Automatic identification of factual claims that are worthy of a fact-check

## About

FactRank ([factrank.org](https://factrank.org/)) is a novel claim detection tool for journalists specifically created for the Dutch language. To the best of our knowledge, this is the first and still the only such tool for Dutch. FactRank thus complements existing online claim detection tools for English and (a small number of) other languages. FactRank performs similarly to claim detection in [ClaimBuster](https://idir.uta.edu/claimbuster/), the state-of-the-art fact-checking tool for English. Our comparisons with a human baseline also indicate that given how much even expert human fact-checkers disagree, there may be a natural “upper bound” on the accuracy of check-worthiness detection by machine-learning methods.

> paper has submitted for publishing, link will hopefully be available soon.

More information: https://factrank.org/about

## Install

```
pip install "git+ssh://git@github.com/lejafar/FactRank.git#egg=factrank"
```

### Develop

requires [poetry](https://github.com/python-poetry/poetry) (>= 1.0.0)

```sh
git clone git@github.com:lejafar/FactRank.git
cd FactRank
make # creates virtual-env and installs pre-commit hooks
```

## Usage

```python
import factrank

text = "Het aantal mensen dat sterft aan covid blijft zorgwekkend oplopen."
(confidence, statement), = factrank.checkworthyness(text)

print("statement": statement)
print("checkworthyness": confidence)
```

## Data

All data is available [here](factrank/data/training).

### The original dataset
The original dataset `statements_{train,test,val}.csv` has been coded by journalism students from the University of Leiden in 2019, more information about the process is available in the paper.

The data was coded in 3 categories:

- **NF:** Not factual
- **FR:** Factual and relevant
- **FNR:** Factual and non-relevant

### User feedback

The online tool, available at [factrank.org](https://factrank.org/) allows users to give feedback on whether they think a statement is worth a factcheck or not, this yield the following binary classification:

- **FR:** Factual and relevant
- **NFR:** Not Factual and relevant

In order to combine this information we can either:

1. only use the positive examples (FR)
2. combine the negative examples (FR+FNR) from the original dataset into a (NFR) category and discard the distinction between them

Currently only the first option has been explored due to time constraints. The original dataset combined with the positive examples can be found [here](factrank/data/training/statements_train_with_positive_feedback_21_03_2020.csv).

## Model

The model is an implementation of [Yoon Kim's Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882). Experiments have been conducted with used more convolutional layers but this did not yield an increase in performance.

### Pre-processing

Pre-processing mainly takes place in [`tokenize.py`](factrank/tokenize.py). It handles cutting text into sentences, cleans up each sentence and adds `NUM` POS-tags.

#### sentencizer

The built-in sentencizer in https://spacy.io/ did not meet our requirements, it did not handle cases like a `.` inside quotes, etc...

#### cleaning

- normalization of quotes, whitespaces, dots, ...
- removal of unwanted symbols `§`, `…`, `=`, `•`
- remove leading and trailing Twitter `@` and `#` tags

### Word embeddings

Word embeddings were taken from https://github.com/clips/dutchembeddings#embeddings (COW, Big). These embeddings are being held static during training for empirical reasons.

The list of embeddings included in this repo [`cow-big-slim.txt`](factrank/data/word_embeddings/cow-big-slim.txt) is a subset, that contains all words that occur in our training data.

These embeddings are also used during inference and are embedded in the pickled statement processor [`factnet.statement-processor.pth`](factrank/data/model/factnet.statement-processor.pth)

### Experiments

Experiments have been done using a (frozen) pre-trained [Bert model](https://arxiv.org/abs/1810.04805) as a backbone, the implementation of `FactNetTransformer` can be found in [`factnet.py`](factrank/factnet.py). The increase in performance was limited, but the increase in required compute was very significant. That's why we're currently using the CNN based model by default.
