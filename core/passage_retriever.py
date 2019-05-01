import numpy as np


class PassageRetrieverService():
    """ """
    def __init__(self):
        pass

    def retrieve(self, document, question):
        """Find the index of the sentence that contains the answer.

        Document + Question -> Int
        """
        scores = [self.score(sent, question) for sent in document.sentences]
        return np.argmax(scores)

    def score(self, sentence, question):
        keyword_match = 0
        ner_match = 0
        first_keyword = None
        last_keyword = None
        for token in sentence.tokens:
            if any([token.match(word) for word in question.features['keywords']]):
                if first_keyword is None:
                    first_keyword = token.index
                last_keyword = token.index
                keyword_match += 1
            if any([token.match(word) for word in question.features['ner']]):
                ner_match += 1
        span = last_keyword - first_keyword
        score = keyword_match + ner_match + (keyword_match / float((span + 1)))
        return score


PassageRetriever = PassageRetrieverService()
