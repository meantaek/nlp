import io
import os


class QuestionFormulatorService():
    """ """
    def __init__(self):
        with io.open(os.path.abspath('./configs/stopwords.txt'), encoding='utf-8') as f:
            self.stopwords = set([word.strip() for word in f.readlines()])

    def formulate(self, sentence):
        """Create a query out of a sentence."""
        keywords = []
        ner = []
        for token in sentence.tokens:
            if token.ner != 'O':
                ner.append(token)
            if token.originalText not in self.stopwords and \
                token.originalText.lower() not in self.stopwords:
                keywords.append(token)
        features = {
            'keywords': keywords,
            'ner': ner
        }
        return features

QuestionFormulator = QuestionFormulatorService()
