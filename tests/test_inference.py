import pytest
import factrank


@pytest.fixture
def model():
    return factrank.get_model()


def test_inference_positive_example(model):
    (prob, sentence), = model.checkworthyness("Het aantal mensen dat sterft aan covid blijft zorgwekkend oplopen.")
    assert prob > 0.9


def test_inference_negative_example(model):
    # NOTE: Feitelijke bewering (Fransen en Nederlanders kopen op Belgische sites).
    #       Woorden als “gelukkig”, “stilaan”, kunnen doen vermoeden dat het om een
    #       relevante verandering gaat. Er is evenwel te weinig context om dat in te schatten.
    #       De claim verraadt ook weinig controverse hierover. Dus Feitelijk Niet-Relevant.
    (prob, sentence), = model.checkworthyness(
        "De Fransen en de Nederlanders kopen gelukkig stilaan ook heel graag op Belgische sites.")
    assert prob < 0.7
