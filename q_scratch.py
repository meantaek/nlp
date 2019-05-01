# from nltk.tree import Tree
# from nltk.parse.corenlp import CoreNLPParser
# from nltk.tag.stanford import CoreNLPNERTagger
# from nltk.tokenize import sent_tokenize
# import os
# import io

# tagger = CoreNLPNERTagger(url='http://nlp01.lti.cs.cmu.edu:9000/')
# text = tagger.tag('The quick brown fox jumps over the lazy dog.')

# parser = CoreNLPParser(url='http://nlp01.lti.cs.cmu.edu:9000/')
# parse = parser.raw_parse("John Smith, a timely person, went to the party.")

# cool = parser.parse_text("After running around for a bit, John went to the party.")

# sent = Tree('ROOT', [Tree('S', [Tree('NP', [Tree('NP', [Tree('NNP', ['John']), 
#     Tree('NNP', ['Smith'])]), Tree(',', [',']), Tree('NP', [Tree('DT', ['a']), 
#     Tree('JJ', ['timely']), Tree('NN', ['person'])]), Tree(',', [','])]), 
# Tree('VP', [Tree('VBD', ['went']), Tree('PP', [Tree('TO', ['to']), Tree('NP', 
#     [Tree('DT', ['the']), Tree('NN', ['party'])])])]), Tree('.', ['.'])])])


#tagger = CoreNLPNERTagger(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')
#parser = CoreNLPParser(url='http://nlp01.lti.cs.cmu.edu:9000/', encoding='utf8')

#print(tagger.tag(["I", "love", "September"]))

def check_lab(node, lab):
    if isinstance(node,Tree):
        return any([node.label() == x for x in lab])
    else:
        return False

def get_proper_noun(NP):
    name = []
    for subtree in NP.subtrees():
        if check_lab(subtree, ["NNP", "NNPS"]):
            name.extend(subtree.leaves())
    return name

def get_parts(tree):
    NP, VP = None, None
    for node in (list(tree)[0]):
        lab = node.label()
        if lab == "NP":
            NP = node
        elif lab == "VP":
            VP = node
    return NP, VP


def get_who(NP, VP, NNP):
    tags = generate_tags(NNP)
    q = ""
    if tags[-1][1] == 'PERSON':
        q = " ".join(["Who"] + VP.leaves())
    else:
        q = " ".join(["What"] + VP.leaves())
    q = "".join(q+"?")
    return q

def find_qs(tree):
    qs = []
    NP, VP = get_parts(tree)
    if NP == None or VP == None:
        return None
    NNP = get_proper_noun(NP)
    if len(NNP) > 0:
        who = get_who(NP, VP, NNP)
        qs.append(who)

    return qs

def generate_qs(trees):
    questions = []
    for tree in trees:
        tree = next(tree)
        # with io.open('wow.txt', 'w', encoding='utf8') as f:
        #     f.write(str(tree))
        if list(tree)[0].label() == "S":
            new_qs = find_qs(tree)
            if new_qs != None:
                questions.extend(new_qs)
    return questions

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

def main():
    filename = os.path.join('data', 'a1.txt')
    with io.open(filename, 'r', encoding='utf8') as f:
        sentences = f.read()

    # sentences = "John Smith, a timely person, went to the party. Juliet was a very nice French woman."
    trees = generate_trees(sentences)
    questions = generate_qs(trees)
    with io.open('wow.txt', 'w', encoding='utf8') as f:
        for q in questions:
            f.write(q + "\n")
    # print(questions)

#main()


# sent_dict = {'NP':None, 'VP':None, 'proper':False, 'single_noun':False,
#                 'past_verb': False, 'main_verb': None, 'PP': None,
#                 'location':False, 'time':False}

# sent = "Charley Smith, a perfect man, went to the park and swam."
# tree = parser.raw_parse(sent)
# tree = next(tree)

# for t in tree.subtrees():
#     if tree.label() == 'S': tree = t
#     break


# NP, VP = None, None
# for node in (list(tree)[0]):
#     if check_lab(node, ['NP']):
#         NP = node
#     elif check_lab(node, ['VP']):
#         VP = node
# sent_dict['NP'] = NP
# sent_dict['VP'] = VP

# NNS = []
# NNP = []
# NNPS = []
# first_level_NP = list(next(NP.subtrees()))[0]
# for subtree in first_level_NP:
#     if check_lab(subtree, ['NNS']): NNS.extend(subtree.leaves())
#     elif check_lab(subtree, ['NNP']): NNP.extend(subtree.leaves())
#     elif check_lab(subtree, ['NNPS']): NNPS.extend(subtree.leaves())

# sent_dict['proper'] = NNP + NNPS if len(NNP)>0 or len(NNPS)> 0 else None
# sent_dict['single_noun'] = False if len(NNS)+len(NNPS)>0 else True


# first_level_VP = next(VP.subtrees())
# main_verb = None
# for i, subtree in enumerate(first_level_VP):
#     if not isinstance(subtree, Tree): continue
#     lab = subtree.label()
#     if i == 0 and lab[0] == "V":
#         main_verb = subtree.leaves()[0]
#         sent_dict['past_verb'] = True if check_lab(subtree, ['VBD', 'VBN']) else False

#     elif i > 0 and lab == "VP":
#         first_leaf = list(subtree)[0]
#         if first_leaf.label()[0] == "V":
#             if main_verb == None:
#                 main_verb = first_leaf.leaves()[0]
#             else:
#                 main_verb = "not simple"
#             sent_dict['past_verb'] = True if check_lab(first_leaf, ['VBD', 'VBN']) else False
#             break
# sent_dict['main_verb'] = main_verb


# PP = None
# for node in VP.subtrees():
#     if check_lab(node, ["PP"]):
#         PP = node.leaves()
# sent_dict['PP'] = PP

# PP_tags = tagger.tag(PP)
# for tag in PP_tags:
#     sent_dict['location'] = tag if tag in ['CITY', 'STATE_OR_PROVINCE', 'COUNTRY'] else False
#     sent_dict['time'] = tag if tag in ['DATE', 'TIME'] else False
