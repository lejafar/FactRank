import pandas as pd
import pathlib
from sklearn.externals import joblib

import helper
import extractor

def load_model(model_version):
    """ Load pre-trained model """
    model_path = pathlib.Path(__file__).parent / f"pre-trained-models/{model_version}.pkl"
    return joblib.load(str(model_path))

class Inferencer:

    def __init__(self, model_version = "v0.2.0"):
        self.model = load_model(model_version)

    def predict_proba(self, statement):
        statement = pd.DataFrame({'content': [statement]})
        return self.model.predict_proba(statement)[0][1]
