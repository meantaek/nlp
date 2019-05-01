import sys
import os
sys.path.append(os.getcwd())

from core.question_generator import generate_questions

if __name__ == '__main__':
    generate_questions(sys.argv[1], int(sys.argv[2]))
