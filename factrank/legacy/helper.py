#!/usr/bin/env python3
"""
Custom feature transformer classes allowing for easy predictions

extractor.py requires the pattern package for python3 to be installed
using the development brach https://github.com/clips/pattern#installation
"""
__author__ = "Rafael Hautekiet"
__copyright__ = "Copyright 2017, Knowledge and the Web Project"
__credits__ = ["Brecht Laperre", "Ivo Merchiers", "Rafael Hautekiet"]
__version__ = "1.0.0"
__maintainer__ = "Rafael Hautekiet"
__email__ = "rafaelhautekiet@student.kuleuven.be"
__status__ = "Development"

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from extractor import Extractor

class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        """
        if key is part of data then preprocessing is already done
        ex. sentence of POS-tags or sentence of lemma_POS-tags
        """
        if self.key in data:
            return data[self.key]
        else:
            return list(map(lambda s: Extractor(s)[self.key], data.ix[:,0]))

class ArrayCaster(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self
    def transform(self, data):
        return np.transpose(np.matrix(data))
