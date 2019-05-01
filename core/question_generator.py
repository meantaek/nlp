from nltk.tree import Tree
from nltk.parse.corenlp import CoreNLPParser
from nltk.tag.stanford import CoreNLPNERTagger
from nltk.tokenize import sent_tokenize
import os
import io
import argparse



# rules =  sent_dict = {'NP':None, 'VP':None, 'proper':None, 'plural_noun':False,
#                         'past_verb': False, 'main_verb': None, 'PP': [],
#                         'location':False, 'time':False}

rules = [{'proper': 'person', 'format':["Who", 'VP']},
            {'proper': 'place', 'format':["What place", 'VP']},
            {'proper': 'date', 'format':["What date", 'VP']},
            {'proper': 'time', 'format':["What time", 'VP']},
            {'proper': 'None', 'format':["What", 'VP']},
            {'location': True, 'simple_verb':True, 'past_verb':False,
                        'format':["Where does", "NP", "main_verb"]}]

def make_q(sent_dict, rule):
    keys = ['NP','VP', 'main_verb']
    q = ""
    for part in rule['format']:
        if part in keys:
            q += sent_dict[part] + " "
        else:
            q += part + " "
    return q[:-1] + "?"


def check_rule(sent_dict, rule):
    for el in rule:
        if el == 'format': continue
        if rule[el] != sent_dict[el]:
            return False
    return True

def gen_qs(sent_dict):
    questions = []
    for rule in rules:
        if check_rule(sent_dict, rule):
            q = make_q(sent_dict, rule)
            questions.append(q)
    return questions

def gen_all_qs(sent_dicts):
    all_questions = []
    for sent_dict in sent_dicts:
        qs = gen_qs(sent_dict)
        all_questions.extend(qs)
    return all_questions


tagger = CoreNLPNERTagger(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')
parser = CoreNLPParser(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')

def check_lab(node, lab):
    if isinstance(node,Tree):
        return any([node.label() == x for x in lab])
    else:
        return False

def get_proper_type(proper):
    tags = generate_tags(proper)
    proper_type = 'None'
    tag = tags[-1][1]

    # with io.open('test_qs.txt', 'w', encoding='utf8') as f:
    #     f.write(str(proper) + " " + tag + " " + str(tags) + "\n")

    if tag == 'PERSON':
        proper_type = 'person'
    elif tag in ['LOCATION', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY']:
        proper_type = 'place'
    elif tag in ['DATE', 'TIME']:
        proper_type = tag.lower()
    return proper_type

def get_prep(VP):
    PP = []
    location, time = False, False
    for node in VP.subtrees():
        if check_lab(node, ["PP"]):
            PP = node.leaves()

    if len(PP) > 0:
        PP_tags = tagger.tag(PP)
        for tag in PP_tags:
            location  = tag in ['LOCATION', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY']
            time = tag in ['DATE', 'TIME']
    return PP, location, time

def get_verbs(VP):
    first_level_VP = next(VP.subtrees())
    main_verb = None
    past_verb = False
    simple_verb = True

    for i, subtree in enumerate(first_level_VP):
        if not isinstance(subtree, Tree): continue
        lab = subtree.label()
        if i == 0 and lab[0] == "V":
            main_verb = subtree.leaves()[0]
            if check_lab(subtree, ['VBD', 'VBN']):
                past_verb = False

        elif i > 0 and lab == "VP":
            first_leaf = list(subtree)[0]
            if first_leaf.label()[0] == "V":
                if main_verb == None:
                    main_verb = first_leaf.leaves()[0]
                else:
                    simple_verb = False
                if check_lab(first_leaf, ['VBD', 'VBN']):
                    past_verb = True
                break
    return main_verb, past_verb, simple_verb

def get_nouns(NP):
    plural = False
    proper = []
    for subtree in NP.subtrees():

        if check_lab(subtree, ['NNS']):
            plural = True
        elif check_lab(subtree, ['NNP']):
            proper.extend(subtree.leaves())
        elif check_lab(subtree, ['NNPS']):
            plural = True
            proper.extend(subtree.leaves())
    return plural, proper

def get_phrases(tree):
    NP, VP = None, None
    for node in (list(tree)[0]):
        if check_lab(node, ['NP']):
            NP = node
        elif check_lab(node, ['VP']):
            VP = node
    return NP, VP

def fill_dict(tree, sent_dict):
    # Noun and Verb Phrases
    NP, VP = get_phrases(tree)

    if NP != None:
        sent_dict['NP'] = " ".join(NP.leaves())
        sent_dict['proper'] = 'None'

        plural, proper = get_nouns(NP)
        sent_dict['plural_noun'] = plural

        if len(proper) > 0:
            proper_type = get_proper_type(proper)
            sent_dict['proper'] = proper_type

    if VP != None:
        sent_dict['VP'] = " ".join(VP.leaves())

        main_verb, past_verb, simple_verb = get_verbs(VP)
        sent_dict['main_verb'] = main_verb
        sent_dict['past_verb'] = past_verb
        sent_dict['simple_verb'] = simple_verb

        PP, location, time = get_prep(VP)
        sent_dict['PP'] = " ".join(PP)
        sent_dict['location'] = location
        sent_dict['time'] = time

    return sent_dict


def generate_dicts(trees):
    sent_dicts = []
    for tree in trees:
        # Initial Sentence Dictionary
        sent_dict = {'NP':None, 'VP':None, 'proper':None, 'plural_noun':False,
                        'past_verb': False, 'main_verb': None, 'simple_verb':True,
                        'PP': [],'location':False, 'time':False}

        tree = next(tree)
        if list(tree)[0].label() == "S":
            new_dict = fill_dict(tree, sent_dict)
            sent_dicts.append(new_dict)
    return sent_dicts

def generate_tags(words):
    tags = tagger.tag(words)
    return tags

def generate_trees(sentences):
    # trees = parser.parse_text(sentences)
    sentences = sent_tokenize(sentences)
    trees = []
    for sent in sentences:
        try:
            tree = parser.raw_parse(sent)
            trees.append(tree)
        except:
            continue
    return trees

def generate_questions(filename, nquestions):

    with io.open(filename, 'r', encoding='utf8') as f:
        sentences = f.read()

    trees = generate_trees(sentences)
    sent_dicts = generate_dicts(trees)
    questions = gen_all_qs(sent_dicts)

    for q in questions[:nquestions]:
        print(q)
