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
from sklearn.utils import shuffle, resample
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import SVC
from sklearn import metrics
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

# TODO: Add recognized entities to featureUnion
# TODO: Add noun-chuncks to featureUnion

def downsample(majority, minority):
    """ Downsample majority """
    majority_downsampled = resample(majority,
                                    replace=False,
                                    n_samples=len(minority),
                                    random_state=33)
    return pd.concat([majority_downsampled,minority])

sentence_data = pd.read_csv("data/sentences_dump_20.12.csv")
sentence_data = shuffle(sentence_data)
# Remove Useless Statements from training data
sentence_data = sentence_data[sentence_data.category != "US"]
sentence_data.category.replace({"CFS": 1, "NFS": 0, "UFS": 0}, inplace=True)
category_names = ['NFS+UFS','CFS']
sentence_data = downsample(sentence_data[sentence_data.category == 0],
                           sentence_data[sentence_data.category == 1])

sentence_data.category.value_counts()

sentence_target = sentence_data.pop("category")

##################################################################
# CREATING MODEL AS A PIPELINE OF FEATURE UNION AND A LINEAR SVM #
##################################################################

# UNION OF ALL FEATURES EXTRACTED FROM SENTENCE
features = FeatureUnion([
    ("words", Pipeline([("cont", FeatureSelector(key='content')),
                        ('vect', CountVectorizer(ngram_range=(1,2),
                                                 max_df=0.2,
                                                 min_df=3,
                                                 stop_words=get_stop_words('nl'))),
                        ('tfidf', TfidfTransformer(use_idf=True,
                                                   sublinear_tf=False))])),
    ("lempos", Pipeline([("cont", FeatureSelector(key='content',  e_key='LEMMA_POS')),
                         ('vect', CountVectorizer(ngram_range=(1,2),
                                                  max_df=0.2,
                                                  lowercase=False,
                                                  min_df=3)),
                         ('tfidf', TfidfTransformer(use_idf=True,
                                                    sublinear_tf=False))])),
    ("possen", Pipeline([("cont", FeatureSelector(key='content', e_key='POS_SENT')),
                         ('vect', CountVectorizer(ngram_range=(1,3),
                                                  max_df=0.5,
                                                  lowercase=False,
                                                  min_df=4)),
                         ('tfidf', TfidfTransformer(use_idf=True,
                                                    sublinear_tf=False))])),
    ("length", Pipeline([("cont", FeatureSelector(key='content', e_key='LENGTH')),
                         ('caster', ArrayCaster())])),
    ("pol",    Pipeline([("cont", FeatureSelector(key='content', e_key='POL')),
                         ('caster', ArrayCaster())])),
    ("subj",   Pipeline([("cont", FeatureSelector(key='content', e_key='SUBJ')),
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
feature_pipe_SVM.fit(sentence_data, sentence_target)
predicted = cross_val_predict(feature_pipe_SVM,
                              sentence_data,
                              sentence_target,
                              cv=10)

##################################################################
#                          VIZUALIZATION                         #
##################################################################

# http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
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

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

##################################################################
#                       EXPORT TRAINED MODEL                     #
##################################################################

joblib.dump(feature_pipe_SVM, 'trained_model.pkl')

##################################################################
#                         OUTPUT FEEDBACK                        #
##################################################################

if __name__ == "__main__":
    print(metrics.classification_report(sentence_target,
                                        predicted,
                                        target_names=category_names))

    # Compute confusion matrix
    cnf_matrix = metrics.confusion_matrix(sentence_target, predicted)

    # Plot normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix,
                          classes=category_names,
                          normalize=True,
                          title='Normalized confusion matrix')
    plt.tight_layout()
    plt.savefig('cnf_matrix.pdf')
