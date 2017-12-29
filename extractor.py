#!/usr/bin/env python3
"""
Exctractor class enables retrieving all nlp features from `sentence`.

Designed for python3 which requires the pattern package to be installed
using the development brach https://github.com/clips/pattern#installation
"""
__author__ = "Ivo Merchiers"
__copyright__ = "Copyright 2017, Knowledge and the Web Project"
__credits__ = ["Brecht Laperre", "Ivo Merchiers", "Rafael Hautekiet"]
__version__ = "1.0.0"
__maintainer__ = "Ivo Merchiers"
__email__ = "ivo.merchiers@student.kuleuven.be"
__status__ = "Development"

from pattern.nl import sentiment, parsetree, lemma, singularize

# import spacy
# nlp = spacy.load('nl')

postags = [u'CC', u'CD', u'DT', u'EX', u'FW', u'IN', u'JJ', u'JJR', u'JJS', u'LS', u'MD', u'NN', u'NNS', u'NNP', u'NNPS', u'PDT', u'POS', u'PRP', u'PRP$',
           u'RB', u'RBR', u'RBS', u'RP', u'SYM', u'TO', u'UH', u'VB', u'VBZ', u'VBP', u'VBD', u'VBN', u'VBG', u'WDT', u'WP', u'WP$', u'WRB', u'.', u',', u':', u'(', u')']

class Extractor:

    """
    Exctractor class enables retrieving all nlp features from `sentence`.
    """

    def __init__(self, sentence):
        self.sentence = sentence
        tree = parsetree(sentence, lemmata=True)
        # tree is actually a sentence in term of pattern definitions
        self.tree = tree[0]
        self.pcounts = self.countPosTags()
        #self.ecounts = self.countEntities()

    def __getitem__(self, k):
        if k == "LEMMA_SENT":
            return self.lemmataSentence()
        elif k == "LEMMA_POS":
            return self.lemmataPosTagSentence()
        elif k == "POS_SENT":
            return self.posTagSentence()
        elif k == "LENGTH":
            return len(self.sentence)
        elif k == "POL":
            return self.polarity()
        elif k == "SUBJ":
            return self.subjectivity()

    def change(self, sentence):
        self.sentence = sentence
        tree = parsetree(sentence, lemmata=True)
        self.tree = tree[0]

    def sent(self):
        """
        :returns: (polarity, subjectivity)
        """
        return sentiment(self.sentence)

    def polarity(self):
        return round(self.sent()[0], 4)

    def subjectivity(self):
        return round(self.sent()[1], 4)

    def parsedSentence(self):
        base = self.tree.words
        return [str(b) for b in base]

    def lemmataSentence(self):
        base = self.tree.lemmata
        base = ' '.join(base)
        return base

    def posTagSentence(self):
        wordlist = self.tree.words
        pos = map(lambda x: x.type, wordlist)
        pos_sent = ' '.join(pos)
        return pos_sent

    def lemmataPosTagSentence(self):
        wordlist = self.tree.words
        base = list(self.tree.lemmata)
        pos = list(map(lambda x: x.type, wordlist))
        lem_pos_sent = ' '.join([ lem + "_" + pos for lem, pos in zip(base,pos)])
        return lem_pos_sent

    def countPosTags(self):
        wordlist = self.tree.words
        pos = list(map(lambda x: x.type, wordlist))
        counts = {}
        for i in range(0, len(postags)):
            counts[postags[i]] = sum(map(lambda x: x == postags[i], pos))
        return counts

    def nounChunks(self):
        raise Error('Not implemented')

    # def countEntities(self):
    #     doc = nlp(self.sentence)
    #     ecounts = {'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
    #     for ent in doc.ents:
    #         ecounts[ent.label_] += 1
    #     return ecounts

# Execute following test, only if this file is ran explicitly
if __name__ == "__main__":
    sentence = u'Ivo Merchiers zegt dat hij graag melk drinkt'
    fe = featureExtractor(sentence)
    print(fe.lemmataPosTagSentence(),fe.posTagSentence())
