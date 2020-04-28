#!/usr/bin/env python3
"""
Preprocess data, construct pipeline, train SVM and export model.

Designed for python3 which requires the pattern package to be installed
using the development brach https://github.com/clips/pattern#installation
"""

# Built-in modules
import itertools

# Third-party modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.externals import joblib
from stop_words import get_stop_words

# Local modules
from helper import FeatureSelector, ArrayCaster

__author__ = "Rafael Hautekiet"
__copyright__ = "Copyright 2017, Knowledge and the Web Project"
__credits__ = ["Brecht Laperre", "Ivo Merchiers", "Rafael Hautekiet"]
__version__ = "1.0.0"
__maintainer__ = "Rafael Hautekiet"
__email__ = "rafaelhautekiet@student.kuleuven.be"
__status__ = "Development"

sentence_data = pd.read_csv("../data/training/statements.csv")
# Remove Useless Statements from training data
sentence_data = sentence_data[sentence_data.label != "ERR"]
sentence_data.label.replace({"FR": 0, "FNR": 1, "NF": 2}, inplace=True)
category_names = ['FR', 'FNR', 'NF']

sentence_target = sentence_data.pop("label")

################################################################################
#        CREATING MODEL AS A PIPELINE OF FEATURE UNION AND A LINEAR SVM        #
################################################################################

# UNION OF ALL FEATURES EXTRACTED FROM SENTENCE
features = FeatureUnion([
    ("words", Pipeline([("cont", FeatureSelector(key='statement')),
                        ('vect', CountVectorizer(ngram_range=(1,1),
                                                 max_df=0.5,
                                                 min_df=1,
                                                 stop_words=get_stop_words('nl'))),
                        ('tfidf', TfidfTransformer(use_idf=True,
                                                   sublinear_tf=False))])),
    ("lempos", Pipeline([("cont", FeatureSelector(key='LEMMA_POS')),
                         ('vect', CountVectorizer(ngram_range=(1,2),
                                                  max_df=0.4,
                                                  lowercase=False,
                                                  min_df=2)),
                         ('tfidf', TfidfTransformer(use_idf=True,
                                                    sublinear_tf=False))])),
    ("possen", Pipeline([("cont", FeatureSelector(key='POS_SENT')),
                         ('vect', CountVectorizer(ngram_range=(1,2),
                                                  max_df=0.6,
                                                  lowercase=False,
                                                  min_df=3)),
                         ('tfidf', TfidfTransformer(use_idf=True,
                                                    sublinear_tf=False))])),
    ("length", Pipeline([("cont", FeatureSelector(key='LENGTH')),
                         ('caster', ArrayCaster())])),
    ("pol",    Pipeline([("cont", FeatureSelector(key='POL')),
                         ('caster', ArrayCaster())])),
    ("subj",   Pipeline([("cont", FeatureSelector(key='SUBJ')),
                         ('caster', ArrayCaster())]))
  ])

feature_pipe_SVM = Pipeline([("features", features),
                             ('clf', SVC(kernel='linear',
                                         class_weight='balanced',
                                         random_state=33,
                                         max_iter=-1, # no limit
                                         probability=True
                                         ))
                            ])

# TRAIN MODEL AND APPLY 10 FOLD CROSSVALIDATION FOR EVALUATION
feature_pipe_SVM.fit(sentence_data,sentence_target)
predicted = cross_val_predict(feature_pipe_SVM,
                              sentence_data,
                              sentence_target,
                              n_jobs=-1,
                              cv=10)

################################################################################
#                                VIZUALIZATION                                 #
################################################################################

# scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Purples):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)

    fig = plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig('cnf_matrix.svg')


################################################################################
#                             EXPORT TRAINED MODEL                             #
################################################################################

joblib.dump(feature_pipe_SVM, 'trained_model.pkl')

################################################################################
#                               OUTPUT FEEDBACK                                #
################################################################################

if __name__ == "__main__":
    print(classification_report(sentence_target,
                                predicted,
                                target_names=category_names))

    # Compute confusion matrix
    cnf_matrix = metrics.confusion_matrix(sentence_target, predicted)

    # Plot normalized confusion matrix

    plot_confusion_matrix(cnf_matrix,
                          classes=category_names,
                          normalize=True,
                          title='Normalized confusion matrix')
