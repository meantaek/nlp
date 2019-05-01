from nltk.parse.corenlp import CoreNLPParser, CoreNLPDependencyParser


parser = CoreNLPParser(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')
depparser = CoreNLPDependencyParser(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')


class Document():
    """ """
    def __init__(self, params):
        self.sentences = [Sentence(sent) for sent in params['sentences']]


class Sentence():
    """ """
    def __init__(self, params):
        self.depgraph = depparser.make_tree(params)
        self.tree = parser.make_tree(params)
        self.index = params['index']
        self.tokens = [Token(token) for token in params['tokens']]
        self.plaintext = ' '.join([token.originalText for token in self.tokens])


class Token():
    """ """
    def __init__(self, params):
        self.after = params.get('after', '')
        self.before = params.get('before', '')
        self.characterOffsetBegin = params.get('characterOffsetBegin', 0)
        self.characterOffsetEnd = params.get('characterOffsetEnd', 0)
        self.index = params.get('index', 0)
        self.lemma = params.get('lemma', '')
        self.ner = params.get('ner', '')
        self.originalText = params.get('originalText', '')
        self.pos = params.get('pos', '')
        self.word = params.get('word', '')

    def match(self, other, orig=True, pos=True, ner=False, lemma=False):
        if orig and self.originalText != other.originalText:
            return False
        if pos and self.pos != other.pos:
            return False
        if ner and self.ner != other.ner:
            return False
        if lemma and self.lemma != other.lemma:
            return False
        return True
