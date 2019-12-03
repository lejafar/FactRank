import pytest
import factrank

def get_checkworthy_sentences():
    return ["Eén op vijf Belgen loopt kans op armoede en sociale uitsluiting.",
            "Multinationals als Shell en Amazon dragen niets bij aan de financiering van onze collectieve voorzieningen.",
            "Ons aantal verpleegkundigen per ziekenhuisbed zit op het niveau van Bulgarije en Griekenland.",
            "Met 30.000 doden per jaar zijn harten vaatziekten de voornaamste doodsoorzaak in België.",
            "Eén op de vier volwassen krijgt vroeg of laat met psychische problemen te maken.",
            "Een quotum verbetert de positie van de Nederlandse vrouw gewoon niet.",
            "Anno 2019: de loonkloof tussen mannen en vrouwen blijkt verder te zijn gegroeid!"]

@pytest.mark.parametrize("sentence", get_checkworthy_sentences())
def test_basic(sentence):
    (prob, _), = factrank.checkworthyness(sentence, suffix='factnet')
    print(prob)
    assert prob > 0.8

@pytest.mark.parametrize("sentence", get_checkworthy_sentences())
def test_bert_basic(sentence):
    (prob, _), = factrank.checkworthyness(sentence, suffix='factnetbert')
    print(prob)
    assert prob > 0.1

def get_non_checkworthy_sentences():
    return ["Aanplanting 1000 bomen in natuurgebied Berendries.",
            "Net als iedereen eet ik liever kip hawaï of kip curry dan kip salmonella.",
            "Nu samenwerken om bedreigde bosgebieden beter te beschermen.",
            "@FirenzeJudy 'Vluchtelingen' zijn zoals de naam doet vermoeden op de 'vlucht'.",
            "Hoe kun je een huidige elektrische auto met batterijen goed recyclen?",
            "Vinnie Fucking Stigma die je aankondigt."]

@pytest.mark.parametrize("sentence", get_non_checkworthy_sentences())
def test_bert_extended(sentence):
    (prob, _), = factrank.checkworthyness(sentence, suffix='factnetbert')
    print(prob)
    assert prob < 0.3




