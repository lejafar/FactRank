import spacy
import re
import unicodedata

class Tokenize(object):
    def __init__(self):
        self.nlp = spacy.load('nl_core_news_sm')

    @staticmethod
    def clean(sentence):
        # normalize unicode equivalence
        sentence = unicodedata.normalize('NFC', sentence)
        # normalize single quotes
        sentence = re.sub(r"’","'", sentence)
        sentence = re.sub(r"‘","'", sentence)
        # normalize double quotes
        sentence = re.sub(r"”","\"", sentence)
        sentence = re.sub(r"„","\"", sentence)
        sentence = re.sub(r"“","\"", sentence)
        # normalize dash
        sentence = re.sub(r"—","-", sentence)
        sentence = re.sub(r"–","-", sentence)
        # replace double punctuations
        sentence = re.sub(r"\?+","?", sentence)
        sentence = re.sub(r"\!+","!", sentence)
        sentence = re.sub(r"\,",",", sentence)
        # different whitespace representations
        sentence = re.sub(r" "," ", sentence)
        sentence = re.sub(r"­"," ", sentence)
        # remove unclosed brackets/quotes
        sentence = re.sub(r"^ *\( ?(?!.*\))","", sentence) # remove unclosed brackets
        sentence = re.sub(r"^ *\' ?(?!.*\')","", sentence) # remove single quotes
        sentence = re.sub(r"^ *\" ?(?!.*\")","", sentence) # remove double quotes
        # remove unwanted stuff
        sentence = re.sub(r"^ +","", sentence)
        sentence = re.sub(r"\n$","", sentence)
        sentence = re.sub(r"§","", sentence)
        sentence = re.sub(r"[A-Z ]+: <<","", sentence)
        # remove point at the end of sentence
        sentence = re.sub(r"\.$","", sentence)
        # clean dirt
        sentence = re.sub(r"…","...", sentence)
        sentence = re.sub(r"[\*\n\\…\=•\[\]\|]", "", sentence)
        return sentence

    def tokenizer(self, sentence):
        return [tok.text for tok in self.nlp.tokenizer(self.clean(sentence).lower()) if tok.text != " "]
