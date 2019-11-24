import pathlib

from .factnet import FactNet, FactNetBert
from .options import Options
from .log import init_package_logger

model_map = {'factnet': FactNet, 'factnetbert': FactNetBert}

_model = {}
def get_model(suffix='factnet'):
    global _model
    if _model.get(suffix) is None:
        run_path = pathlib.Path(__file__).parent / f'data/model/{suffix}'
        options = Options.load(run_path / f'{suffix}.options.yml')
        init_package_logger(options)
        _model[suffix] = model_map[suffix](options)
    return _model[suffix]

def infer(text_or_sentences, **kwargs):
    return get_model(**kwargs).infer(text_or_sentences)

def checkworthyness(text_or_sentences, **kwargs):
    return get_model(**kwargs).checkworthyness(text_or_sentences)


