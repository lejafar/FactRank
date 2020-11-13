import pathlib

from .factnet import FactNet
from .options import Options
from .log import init_package_logger

_model = None


def get_model():
    global _model
    if _model is None:
        run_path = pathlib.Path(__file__).parent / 'data/model'
        options = Options.load(run_path / 'factnet.options.yml')
        init_package_logger(options)
        _model = FactNet(options)
    return _model


def infer(text_or_sentences):
    return get_model().infer(text_or_sentences)


def checkworthyness(text_or_sentences, **kwargs):
    return get_model().checkworthyness(text_or_sentences, **kwargs)
