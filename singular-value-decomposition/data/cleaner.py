import json
import os

from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag, word_tokenize


def loadRaw(directory):
    documents = dict()

    for filename in os.listdir(directory):
        if filename[-3:] == 'txt':
            with open(os.path.join(directory, filename), 'r') as infile:
                documents[filename] = infile.read()

    return documents


allWords = None


def words():
    global allWords
    with open('data/one-grams.txt', 'r') as infile:
        allWords = [line.strip() for line in infile]

    return set(allWords)


# Extract a list of tokens from a cleaned string.
def tokenize(s):
    stopWords = set(stopwords.words('english'))
    wordsToKeep = words() - stopWords

    return [x.lower() for x in word_tokenize(s)
            if x in wordsToKeep and len(x) >= 3]


def wordnetPos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def process():
    print("Loading...")
    documentDict = loadRaw('data/cnn-stories')
    documents = []

    print("Cleaning...")
    i = 0
    for filename, documentText in documentDict.items():
        tokens = tokenize(documentText)
        tagged_tokens = pos_tag(tokens)
        wnl = WordNetLemmatizer()
        stemmedTokens = [wnl.lemmatize(word, wordnetPos(tag)).lower()
                         for word, tag in tagged_tokens]

        documents.append({
            'filename': filename,
            'text': documentText,
            'words': stemmedTokens,
        })
        if i % 100 == 0:
            print(i)
        i += 1

    print("Writing to disk...")
    with open('all_stories.json', 'w') as outfile:
        outfile.write(json.dumps(documents))

    print("Done!")


process()
