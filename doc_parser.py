from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import word_tokenize

from entities import Token

import io
import sys
import os
import nltk

# NOTES To The Group
'''
Hi, I did the Tokenization, NER and POS Tagging. I tried to get the Stanford POS to work, but failed. Instead, I used nltk.pos_tag for POS.
I managed to get StandfordNERTagger to work. We need to set up Java, and make adjustments in Environment Path for Stanford NLTK.
The steps I followed are in this link
https://blog.manash.me/configuring-stanford-parser-and-stanford-ner-tagger-with-nltk-in-python-on-windows-f685483c374a
Both POS and NER spits out a list of tuples with tags.
'''

# These lines have to be outside of the main function to be global objects

# I had to do this to get Java to work.
os.environ['JAVAHOME'] = r"C:\Program Files\Java\jre1.8.0_161\bin"

# Change the path according to your system
stanford_classifier = r'C:\Users\Barry Li\Documents\nlp\project\stanford-ner-2018-02-27\classifiers\english.all.3class.distsim.crf.ser.gz'
stanford_ner_path = r'C:\Users\Barry Li\Documents\nlp\project\stanford-ner-2018-02-27\stanford-ner.jar'

# Creating Tagger Object
stNER = StanfordNERTagger(stanford_classifier, stanford_ner_path)


# Tokenizes the string variable text into list of words.
def tokenize(text):
    return word_tokenize(text)


# Uses StanfordNERTagger. Prints Tags if p is set to True.
def ner_tag(text, p=False):
    tokenized_text = tokenize(text)
    ner_text = stNER.tag(tokenized_text)
    if p is True:
        print(ner_text)
    return ner_text


# Uses nltk.pos_tag(). Prints Tags if p is set to True.
def pos_tag(text, p=False):
    tokenized_text = tokenize(text)
    pos_text = nltk.pos_tag(tokenized_text)
    if p is True:
        print(pos_text)
    return pos_text


def parse_text(text):
    tokenized_text = tokenize(text)
    ner_text = stNER.tag(tokenized_text)
    pos_text = nltk.pos_tag(tokenized_text)
    tokens = []
    for ner, pos in zip(ner_text, pos_text):
        word = ner[0]
        tags = list(ner[1:])
        tags = tags + list(pos[1:])
        token = Token(word, tags)
        tokens.append(token)
    return tokens