from nltk.parse.corenlp import CoreNLPParser
from entities.document import Document, Sentence
from entities.question import Question
import os
import io


parser = CoreNLPParser(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')
parser2 = CoreNLPParser(url='http://nlp02.lti.cs.cmu.edu:9000/', encoding='utf8')


def parse_document(document_text):
    additional_props = {'annotators': 'tokenize,ssplit,ner,parse'}
    try:
        parsed_doc = parser.api_call(document_text, properties=additional_props)
    except Exception:
        try:
            parsed_doc = parser2.api_call(document_text, properties=additional_props)
        except Exception:
            print('CoreNLP api call failed')
            return None
    return Document(parsed_doc)


def parse_questions(question_text):
    additional_props = {'annotators': 'tokenize,ssplit,ner,parse'}
    try:
        parsed_doc = parser.api_call(question_text, properties=additional_props)
    except Exception:
        try:
            parsed_doc = parser2.api_call(question_text, properties=additional_props)
        except Exception:
            print('CoreNLP api call failed')
            return None
    return [Question(Sentence(question)) for question in parsed_doc['sentences']]
