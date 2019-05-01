import sys
import os
import io
import warnings
warnings.filterwarnings('ignore')
sys.path.append(os.getcwd())

from core import doc_parser
from core.passage_retriever import PassageRetriever
from core.answer_processor import AnswerProcessor


def main(docpath, questionpath):
    with io.open(docpath, 'r', encoding='utf8') as f:
        doctext = f.read()
    document = doc_parser.parse_document(doctext)

    with io.open(questionpath, 'r', encoding='utf8') as f:
        questiontext = f.read()
    questions = doc_parser.parse_questions(questiontext)

    idxes = [PassageRetriever.retrieve(document, q) for q in questions]
    answers = [
        AnswerProcessor.find_answer(document.sentences[idx], q)
        for idx, q in zip(idxes, questions)
    ]
    for answer in answers:
        print(answer)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
