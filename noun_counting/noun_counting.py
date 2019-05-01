import io
import os
import nltk

def get_nouns(corpi):
    nouns = {}
    for key in corpi:
        nouns[key] = [(word,pos) for word,pos in corpi[key] if pos[:2] == "NN"]
    return(nouns)

def get_words(file):
    # Get words and tags from one file
    pos_tags = []
    with io.open(os.path.join('data',file), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            words = [word for word in nltk.word_tokenize(line)]
            pos_tags.extend(nltk.pos_tag(words))
    return(pos_tags)

def get_corpus():
    # Create corpus from all files
    text_files = ["a{}.txt".format(i) for i in range(1,10+1)]
    corpi = {}
    for file in text_files:
        words = get_words(file)
        corpi[file] = words
    return corpi

def main():
    # Get corpus of words for each file files, stored as a dictionary
    corpi = get_corpus()

    # Get and print total number of nouns (stored in dict) in each files
    nouns = get_nouns(corpi)
    with open('filecounts.txt', 'w') as f:   
        for file in nouns:
            f.write(file + " " + str(len(nouns[file])) + "\n")

    # For purposes of error analysis
    # write nouns and their tags to output file
    with io.open('nouns.txt', 'w', encoding='utf-8') as f: 
        nouns1 = nouns['a1.txt']
        f.write("Total: " + str(len(nouns1)) + "\n")
        for noun, pos in nouns1:
            f.write(noun + " " + pos + "\n")

if __name__ == "__main__":
    main()
