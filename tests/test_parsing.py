import pytest

from factrank.tokenize import Tokenize

@pytest.fixture
def tokenizer():
    return Tokenize()

def test_parsing_twitter_dirt(tokenizer):
    # leading tags
    txt = """@NanetteNooteboo @trouw Bedankt, krijg er vaker complimenten over."""
    assert tokenizer.sentencize(txt).__next__() == "Bedankt, krijg er vaker complimenten over."
    txt = """ @NanetteNooteboo @trouw Bedankt @Minister, krijg er vaker complimenten over."""
    assert tokenizer.sentencize(txt).__next__() == "Bedankt @Minister, krijg er vaker complimenten over."
    txt = """Allereerst @NanetteNooteboo @trouw bedankt, krijg er vaker complimenten over."""
    assert tokenizer.sentencize(txt).__next__() == "Allereerst @NanetteNooteboo @trouw bedankt, krijg er vaker complimenten over."

def test_previous_parsing_errors(tokenizer):
    # tripping around !
    txt = """Wel nog even ook ons huiswerk op orde : zo stoten (echt?) wij (in NL) 5 keer (!) meer CO2 uit per persoon dan een Braziliaan."""
    assert tokenizer.sentencize(txt).__next__() == txt
    # check unclosed bracket
    txt = """Wel nog even ook ons huiswerk op orde : zo stoten (echt?"""
    assert len(list(tokenizer.sentencize(txt))) == 0
    # should just pass
    txt = """Nadat het CDA was gedraaid (laat ik het een veranderd standpunt noemen) in de discussie rond het kinderpardon, was er een meerderheid in de Tweede Kamer voor een ruimere interpretatie van de regels."""
    assert tokenizer.sentencize(txt).__next__() == txt
    txt = """En dus kwamen coalitiepartners VVD, CDA, D66 en ChristenUnie tot een eigen asieldeal waarin er nog één keer royaal pardon wordt verleend aan zo'n 700 gezinnen en de regeling daarna verdwijnt."""
    assert tokenizer.sentencize(txt).__next__() == txt

