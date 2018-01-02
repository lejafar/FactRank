#!/usr/bin/env python3
"""
Parse latest transcript of plenary meeting, detect Check-Worthy statements
and save predictions together with feedback to be served on demo page.

helper.py requires the pattern package for python3 to be installed
using the development brach https://github.com/clips/pattern#installation
"""

# Built-in modules
import urllib
import re
import unicodedata
import pickle
import os.path
import sys
import argparse as ap

# Third-party modules
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from scipy.sparse import find

# Local modules
from helper import FeatureSelector, ArrayCaster
from extractor import Extractor

__author__ = "Rafael Hautekiet"
__copyright__ = "Copyright 2017, Knowledge and the Web Project"
__credits__ = ["Brecht Laperre", "Ivo Merchiers", "Rafael Hautekiet"]
__version__ = "1.0.0"
__maintainer__ = "Rafael Hautekiet"
__email__ = "rafaelhautekiet@student.kuleuven.be"
__status__ = "Development"

# SOME GLOBAL VARIABLES

KAMER_BASE_URL = "https://www.dekamer.be"
KAMER_URL = KAMER_BASE_URL + \
    "/kvvcr/showpage.cfm?section=/cricra&language=nl&cfm=dcricra.cfm?type=plen&cricra=cri&count=all"

############ Precompile regular expressions ############
# Note: the sentence regex doesn't handle quotes correctly,
#       this will be updated later on. For now, the predictions
#       are made using the same regex used for trainig
PARTY_NAME_REGEX = r'\(([^\)]+)\):'
pn_regex = re.compile(PARTY_NAME_REGEX)
SENTENCE_REGEX = r' ?((?:[^?!\.\n]|\.[^ A-Z])+(?:!|\.{1,3})) ?'
#                       --------------------     ---------
#                                 1                  2
# 1: A sentence does not contain '?','!','.' or '\n'
#    but does contain '.' not followed by a space and and a Capital letter
# 2: A sentence may end with '!', '.' or '...'
s_regex = re.compile(SENTENCE_REGEX)
# Regex below accepts sentences without a punctuation mark
SENTENCE_REGEX_SOFT = r' ?((?:[^?!\.\n]|\.[^ A-Z])+(?:!|\.{0,3})) ?'
soft_s_regex = re.compile(SENTENCE_REGEX_SOFT)
FILE_NAME_REGEX = r'ip\d+.*(?=\.)'
fn_regex = re.compile(FILE_NAME_REGEX)
########################################################

def load_model():
    """ Load pre-trained model """
    model = joblib.load('trained_model.pkl')
    cat_names = ['NFS+UFS', 'CFS']
    return model, cat_names


def prepForPred(sentences):
    """ Provide model with expected dictionary """
    return pd.DataFrame({'content': sentences})


def save_obj(obj, name):
    """ Save dictionary for later use """
    with open('archive/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def get_all_feature(model):
    """
    Retrieves all n features (columns) that or used by `model`'s one-hot encoding

    :returns: list of feature_names
    """
    feature_names = []
    for transformer in model.named_steps['features'].transformer_list:
        if 'vect' in transformer[1].named_steps:
            feature_names += transformer[1].named_steps['vect'].get_feature_names()
    other_features = ["LENGTH", "POL", "SUBJ"]
    feature_names += other_features
    return feature_names

def get_features(model, sentence):
    """
    Retrieves all non-zero features (columns) found by `model` in `sentence`

    :returns: dictionary of feature names for each sort
    """
    other_features = ["LENGTH", "POL", "SUBJ"]
    non_zero_rows = find(model.named_steps['features'].transform(
        prepForPred([sentence])))[1]
    feature_names = get_all_feature(model)
    features = [feature_names[row] for row in non_zero_rows]
    features = list(set(features))  # remove duplicates
    feature_words = [f for f in features if not any(c.isupper() for c in f)]
    feature_lemma_pos = [f for f in features if '_' in f and not '_' == f[0]]
    feature_pos = [f for f in features if all(
        c.isupper() or c == " " for c in f) and f not in other_features]
    feature_others = [f for f in features if f in other_features]
    return {'words': feature_words,
            'lempos': feature_lemma_pos,
            'pos': feature_pos,
            'other': feature_others}


def get_top_n_featues(model, n, nfsufs):
    """
    Retrieve `n` features with the highest coefficient value in `model`

    :returns: list of `n` most informative CFS features
    """
    clf = model.named_steps['clf']
    class_labels = clf.classes_
    feature_names = get_all_feature(model)
    if nfsufs:
        return [feature_names[j] for j in np.argsort(clf.coef_.toarray())[:,:n][0]]
    else:
        return [feature_names[j] for j in np.argsort(clf.coef_.toarray())[:, -n:][0]]


def indicesOfSublist(sublist, list, start=0):
    """
    :returns: indices of sublist in list start from `start`
    """
    indices = []
    sub_index = 0
    chain = False
    for i, item in enumerate(list[:-len(sublist)]):
        while True:
            if item == sublist[sub_index]:
                # on chain, increase subindex an add i to indices
                sub_index += 1
                indices += [start + i]
                if sub_index == len(sublist):
                    # full sublist is found, try to found next occurence
                    return indices + indicesOfSublist(sublist, list[i:], start=i)
                break
            else:
                indices = []
                # if sub_index !=0, set to 0 and retry current item
                if sub_index:
                    sub_index = 0
                    continue
                break
    return indices

def indicesOfitem(item, list):
    return [i for i, value in enumerate(list) if value == item]


def get_feedback(model, sentence, nfsufs):
    """
    Generate structured feedback based on the non-zero features found by
    `model` in `sentence`. This will be served and parsed by our front-end

    Feedback is provided in the form of list:

    ex.          'Vroeger gold het laagste tarief alleen maar tot 25 000 euro , ...'
    word:        [   0,    0,   0,    0,      0,     0,    0,  0,  0, 1,   1  , ...]
    word_combo:  [   0,    0,   0,    0,      0,     0,    0,  0,  0, 0,   0  , ...]
    lempos:      [   1,    0,   0,    0,      0,     0,    0,  0,  0, 1,   1  , ...]
    lempos_combo:[   0,    0,   0,    0,      0,     0,    0,  0,  0, 0,   0  , ...]
    pos:         [   0,    0,   0,    1,      0,     0,    0,  0,  1, 0,   0  , ...]
    pos_combo:   [   0,    0,   1,    1,      0,     0,    0,  0,  1, 1,   0  , ...]

    This information is parsed by the javascript front-end in order to create
    inline feedback on how the model came to predict CFS level of statement.

    :returns: dictionary of feedback
    """
    cfs_list = get_top_n_featues(model, 500, nfsufs)
    features = get_features(model, sentence)
    extractor = Extractor(sentence)
    word_sentence = [word.lower() for word in extractor.parsedSentence()]
    n = len(word_sentence)
    word_list = [0] * n
    word_combo_list = [0] * n
    for word in features['words']:
        if len(word.split()) == 1:
            indices = indicesOfitem(word, word_sentence)
            for indice in indices:
                word_list[indice] = int(word in cfs_list)
        else:
            indices = indicesOfSublist(word.split(), word_sentence)
            for indice in indices:
                word_combo_list[indice] += int(word in cfs_list)

    lempos_sentence = extractor.lemmataPosTagSentence()
    lempos_list = [0] * n
    lempos_combo_list = [0] * n
    for lempos in features['lempos']:
        if len(lempos.split()) == 1:
            indices = indicesOfitem(lempos, lempos_sentence.split())
            for indice in indices:
                lempos_list[indice] = int(lempos in cfs_list)
        else:
            indices = indicesOfSublist(lempos.split(), lempos_sentence.split())
            for indice in indices:
                lempos_combo_list[indice] += int(lempos in cfs_list)

    pos_sentence = extractor.posTagSentence()
    pos_list = [0] * n
    pos_combo_list = [0] * n
    for pos in features['pos']:
        if len(pos.split()) == 1:
            indices = indicesOfitem(pos, pos_sentence.split())
            for indice in indices:
                pos_list[indice] = int(pos in cfs_list)
        else:
            indices = indicesOfSublist(pos.split(), pos_sentence.split())
            for indice in indices:
                pos_combo_list[indice] += int(pos in cfs_list)
    return {'words': extractor.parsedSentence(),
            'inline': {'word': word_list,
                       'word_combo': word_combo_list,
                       'lempos': lempos_list,
                       'lempos_combo': lempos_combo_list,
                       'pos': pos_list,
                       'pos_combo': pos_combo_list},
            'legend': { 'lempos_legend': lempos_sentence.split(),
                        'pos_legend': pos_sentence.split()},
            'others': {'LENGTH': len(word_sentence),
                       'POL': extractor.polarity(),
                       'SUBJ': extractor.subjectivity()
                       }}


def last_transcript(production= False):
    """
    Check for latest transcript at `KAMER_URL`,
    if `production`, check if transcript has already been parsed,
    parse latest transcript and return list of text from speakers

    Todo: * Make parser more resistant to slight HTML changes

    :returns: list of BS tag objects
    """
    f = urllib.request.urlopen(KAMER_URL)
    html = f.read()  # the HTML code you've written above
    parsed_html = BeautifulSoup(html, "lxml").body.find('table')
    session_urls = parsed_html.select(
        'a[title="Kopieervriendelijke HTML versie"]')
    date = ' '.join(
        session_urls[0].parent.previous_sibling.previous_sibling.contents[0].split())
    last_session_url = session_urls[0].attrs['href']

    if production:
        # In production, so check if last transcript has already been parsed
        if os.path.isfile("archive/PM " + date + ".pkl"):
            return False, last_session_url, date

    # Parse last plenary meeting
    # Note: HTML is automatically produced by MS WORD and is quit messy,
    #       the approach below is highly prone to parsing errors
    pm_html = urllib.request.urlopen(KAMER_BASE_URL + last_session_url).read()
    parsed_pm_html = BeautifulSoup(pm_html, "lxml").body
    speakers = parsed_pm_html.select(
        'p[class="NormalNL"] > span[class="oraspr"] > span[style="mso-ansi-language:NL"] > span')
    return speakers, last_session_url, date

def bulk_predict(model, c_names, text, speaker = {}, ufsnfs=False):
    sentences = s_regex.findall(text)
    if not speaker and "." not in text and "?" not in text:
        sentences = soft_s_regex.findall(text)

    # there is a weird bug where a  leading and trailing quote appears
    if sentences and sentences[0] and sentences[0][0] == "\"":
        sentences[0] = sentences[0][1:]
    if sentences and sentences[-1] and sentences[-1][-1:] == "\"":
        sentences[-1] = sentences[-1][:-1]

    bulk_predictions = []
    for s, sentence in enumerate(sentences):
        sentence = unicodedata.normalize("NFKD", sentence)
        prediction = {}
        if len(sentence.split()) >= 5:
            prepped = prepForPred([sentence])
            feedback = get_feedback(model, sentence, ufsnfs)
            if speaker:
                prediction = speaker.copy()
            prediction['sentence'] = sentence
            prediction['sentence_id'] = s
            prediction['category'] = c_names[model.predict(prepped)[0]]
            if ufsnfs:
                prediction['probability'] = model.predict_proba(prepped)[0][0]
            else:
                prediction['probability'] = model.predict_proba(prepped)[0][1]
            prediction['feedback'] = feedback
            bulk_predictions += [prediction]
    return bulk_predictions

def parse(model, c_names, speakers):
    """
    Loop true html tags that contains a `speaker`'s text, combine text that
    belongs to the same speaker and parse his/her corresponding party.

    :returns: list of predictions each made out of a dictionary
    """
    predictions = []
    for i, speaker in enumerate(speakers):
        name = speaker.next_sibling.replace('\r', '').replace('\n', ' ')
        text_node = speaker.parent.parent.next_sibling
        text = text_node.contents[0]
        party = "Unknown"
        parent = text_node.parent
        # While next is not another speaker, add to current
        while not parent.next_sibling.next_sibling.select('span[class="oraspr"]'):
            parent = parent.next_sibling.next_sibling
            # Skip if non-dutch is found
            if 'class' in parent.attrs and parent.attrs['class'][0] != "NormalNL":
                continue
            text_next = parent.find(text=True, recursive=True)
            # Skip empty parts of text
            if text_next.strip() != "":
                text += ' ' + text_next

        if pn_regex.findall(text):
            party = pn_regex.findall(text)[0]
            text = pn_regex.sub('', text)

        speaker = {'speaker_id': i,
                   'speaker': name,
                   'party': party}

        text = text.replace('\r', '').replace('\n', ' ')
        predictions += bulk_predict(model, c_names, text, speaker = speaker)

    return predictions


if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Parser")
    parser.add_argument("--production", action='store_true')
    args, others = parser.parse_known_args()

    model, c_names = load_model()
    speakers, last_session_url, date = last_transcript(args.production)
    if not speakers:
        sys.exit("Latest transcript from " + date + "(" + last_session_url +
                 ") was already parsed, I'll try again tommorow! ")
    print("Started parsing model ... (this might take a while)")
    parse_dict = {}
    parse_dict['meta'] = {}
    parse_dict['meta']['date'] = date
    parse_dict['meta']['url'] = KAMER_BASE_URL + last_session_url
    parse_dict['predictions'] = parse(model, c_names, speakers)
    parse_dict['meta']['amount'] = len(parse_dict['predictions'])
    file_name = fn_regex.findall(last_session_url)[0] or "unknown"
    save_obj(parse_dict, file_name)
    print("Finished parsing! Saved the dictionary at archive/"+ file_name +".pkl")
