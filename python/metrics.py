"""
This module contains metrics and helpers for those metrics.

All metrics will take in a pair (x, y) and return a non-negative real number.
"""

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import cmudict
from nltk.metrics import edit_distance, jaccard_distance

# NOTE this is a global variable
PHOENOME = cmudict.dict()
TOKENIZER = RegexpTokenizer(r'\w+')

def editDistance(pair):
    return edit_distance(pair[0], pair[1])

def stanzaLen(pair):
    # TODO This is not a metric... strings of the same length map to zero,
    # but are not the same element
    return abs(len(pair[0]) - len(pair[1]))

def getTokenSet(word, option='list'):
    # tokenize only words
    tokens = TOKENIZER.tokenize(word)
    if option == 'set':
        return set(tokens)
    elif option == 'list':
        return tokens

def jaccardDistance(pair):
    ## Split strings by word/punctuation
    wordPair = map(getTokenSet, pair)
    return jaccard_distance(wordPair[0], wordPair[1])

def syllableLen(word):
    """return number of syllables in each stanza"""
    try:
        syllables = [len(list(y for y in x if y[-1].isdigit())) for x in PHOENOME[word.lower()]]
    except:
        syllables = [0]
    return syllables[0]

def lineLen(stanza):
    """return number of lines in each stanza"""
    lineSplit = stanza.split('\n')
    return len(filter(lambda l: l != '', lineSplit))


def avgSyllableDist(pair):
    """difference between syllables/line for each pair"""
    tokenPair = map(getTokenSet, pair)
    # for each stanza: [words] --> int(syllables)
    sumSyllbles = lambda words: sum(map(syllableLen, words))
    syllableCount = [sumSyllbles(s) for s in tokenPair]
    # number of lines for each stanza
    lineCount = [lineLen(s) for s in pair]
    # (syllables, lines)
    dataPair = zip(syllableCount, lineCount)
    # syllables / lines
    dividePair = [ p[0] / float(p[1]) for p in dataPair]
    # difference in syllables per line
    return abs(dividePair[0] - dividePair[1])
