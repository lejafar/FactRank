#!/usr/bin/env python3
"""
Load pre-trained model and provide endpoint for predictions.

helper.py requires the pattern package for python3 to be installed
using the development brach https://github.com/clips/pattern#installation
"""

# Built-in modules
import re
import pickle
import glob
import os

# Third-party modules
import pandas as pd
from scipy.sparse import find
from sklearn.externals import joblib
from flask import Flask, request, jsonify
from flask import make_response
from flask_restful import reqparse, Resource, Api
from flask_cors import CORS, cross_origin

# Local modules
from helper import FeatureSelector, ArrayCaster
from parser import bulk_predict

__author__ = "Rafael Hautekiet"
__copyright__ = "Copyright 2017, Knowledge and the Web Project"
__credits__ = ["Brecht Laperre", "Ivo Merchiers", "Rafael Hautekiet"]
__version__ = "1.0.0"
__maintainer__ = "Rafael Hautekiet"
__email__ = "rafaelhautekiet@student.kuleuven.be"
__status__ = "Development"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
parser = reqparse.RequestParser()
parser.add_argument('sentence')

# LOAD PRE-TRAINED MODEL
model = joblib.load('trained_model.pkl')
cat_names = ['NFS+UFS', 'CFS']

@app.route('/plenair', methods=['GET', 'OPTIONS'])
@cross_origin()
def load_parsed_plenair():
    list_of_files = glob.glob('archive/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    parse_dict = {}
    with open(latest_file, 'rb') as f:
        parse_dict = pickle.load(f)
    n, desc = 100, True  # sort desc and take top n predictions
    parse_dict['predictions'] = sorted(
        parse_dict['predictions'], key=lambda k: k['probability'][1], reverse=desc)[:n]
    return jsonify(parse_dict)


@app.route('/sentence', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def parse_sentences():
    r = '{"Sentence": "nothing found ..."}'
    if request.method == 'POST':
        text = request.get_data().decode('utf-8').replace('\\r', '\r').replace('\\n', '\n')
        bulk = sorted(bulk_predict(model, cat_names, text), key=lambda k: k['probability'][1], reverse=True)
        resp = {'predictions': bulk}
        return jsonify(resp)
    return jsonify(r)

@app.route("/")
def hello():
    return "<h1>Welcome to the <code>FactRank api</code></h1><p>Documentation comming soon!</p>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)
