import spacy
import re
import unicodedata

class Tokenize:

    def __init__(self, options):
        self.nlp = spacy.load('nl_core_news_sm')
        self.sentence_regex = re.compile(r' ?((?:[A-Z@#]|[\"\'][^\n]+?[\"\'] ?)(?:[\"\'][^\n]+?[\"\']|\.{3}|[^?!\.\n]|\.[^ \nA-Z\"\'])*(?:!|\?|\n|\.{1})) ?')

    @staticmethod
    def clean_text(text):
        # normalize unicode equivalence
        text = unicodedata.normalize('NFC', text)
        text = re.sub(r"\r", "", text)
        # normalize single quotes
        text = re.sub(r"’","'", text)
        text = re.sub(r"‘","'", text)
        # normalize double quotes
        text = re.sub(r"”","\"", text)
        text = re.sub(r"„","\"", text)
        text = re.sub(r"“","\"", text)
        # replace linebreak by punctuation when followed by linebreak
        text = re.sub(r"(\"|\')\n", "\g<1>.", text)
        # normalize dash
        text = re.sub(r"—","-", text)
        text = re.sub(r"–","-", text)
        # replace double punctuations
        text = re.sub(r"\?+","?", text)
        text = re.sub(r"\!+","!", text)
        text = re.sub(r"\,",",", text)
        # different whitespace representations
        text = re.sub(r" "," ", text)
        text = re.sub(r"­"," ", text)
        # remove unwanted stuff
        text = re.sub(r"^ +","", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\n$","", text)
        text = re.sub(r"§","", text)
        # clean dirt
        text = re.sub(r"…","...", text)
        text = re.sub(r"[\*\n\\…\=•\[\]\|]", "", text)
        return text

    @staticmethod
    def clean_sentence_for_inference(sentence):
        sentence = Tokenize.clean_text(sentence)
        # remove unclosed brackets/quotes
        sentence = re.sub(r"^ *\( ?(?!.*\))","", sentence) # remove unclosed brackets
        sentence = re.sub(r"^ *\' ?(?!.*\')","", sentence) # remove single quotes
        sentence = re.sub(r"^ *\" ?(?!.*\")","", sentence) # remove double quotes
        # remove unwanted stuff
        sentence = re.sub(r"^ +","", sentence)
        sentence = re.sub(r"[A-Z ]+: <<","", sentence)
        # remove point at the end of sentence
        sentence = re.sub(r"\.$","", sentence)
        # remove quotes when apparent at both ends
        sentence = re.sub(r"^\'(.*)\'$","\g<1>", sentence) # single quotes
        sentence = re.sub(r"^\"(.*)\"$","\g<1>", sentence) # double quotes
        # clean twitter dirt
        sentence = re.sub(r"@#", "", sentence)
        return sentence

    def tokenize(self, sentence):
        return [tok.text for tok in self.nlp.tokenizer(self.clean_sentence_for_inference(sentence).lower()) if tok.text != " "]

    def sentencize(self, text):
        for sentence in self.sentence_regex.findall(self.clean_text(text)):
            if len(sentence.split()) < 3 or len(sentence.split()) > 50:
                continue # too long / too short
            if sentence.count("\"") % 2 or sentence.count("\'") % 2:
                continue # unclosed quotes
            if sentence.count("(") % 2 or sentence.count(")") % 2:
                continue # unclosed brackets
            if sentence.count('#') > len(sentence.split()) / 2:
                continue # probably too many hashtags
            yield sentence.strip()
