from core.question_classifier import QuestionClassifier
from core.question_formulator import QuestionFormulator


class Question():
    """ """

    def __init__(self, sentence):
        self.sentence = sentence
        self.type = QuestionClassifier.classify(self.sentence)
        self.features = QuestionFormulator.formulate(self.sentence)
