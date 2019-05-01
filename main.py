from doc_parser import parse_text
from entities import Token, Pattern, ExtractionRule
import io
import sys


def extract_questions(tokens, rules):
    questions = []
    for rule in rules:
        questions += rule.extract(tokens)
    return questions


def extract_text(text, rules):
    questions = []
    sentences = text.strip().split('.')
    for sentence in sentences:
        tokens = parse_text(sentence)
        new_questions = extract_questions(tokens, rules)
        print(new_questions)
        questions += new_questions
    return questions

if __name__ == '__main__':
    rules = [
        ExtractionRule('[NN] is [NN]', 'What is a [NN] ?', {0: 0}),
        ExtractionRule('[NN] is [JJ]', 'What is a [NN] ?', {0: 0}),
        ExtractionRule('[NNP] is [NN]', 'What is [NNP] ?', {0: 0}),
        ExtractionRule('[NNP] is [JJ]', 'What is [NNP] ?', {0: 0}),
        ExtractionRule('[NN] is in [LOC]', 'Where is [NN] ?', {0: 0}),
        ExtractionRule('[PER] is [NN]', 'Who is [NN] ?', {0: 0})
    ]

    with io.open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()
    print(text)
    print(set(extract_text(text, rules)))
