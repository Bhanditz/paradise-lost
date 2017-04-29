import helpers as hlp
import random
import numpy as np

def reduceStanzasToList(stDict):
    '''
    Take stanzas in dict format and turn them into a flat list.
    The result is the whole book as a list, each element being a stanza
    (Note that we have to sort the books first)
    '''
    # f: 'bookN' --> N
    bookToInt = lambda x: int(x.replace('book', ''))
    # { bookN: [stanzas] } --> [ (N, [stanzas]) ]
    bookList = [ (bookToInt(x), stDict[x]) for x in stDict.keys() ]
    # sort by N (chapter number)
    bookList.sort(key = lambda x: x[0])
    # [ (N, [stanzas]) ] --> [ [stanzas] ]
    stanzaList = map(lambda x: x[1], bookList)
    # flatten stanzas
    flatStanzas = hlp.flattenListOnce(stanzaList)
    return flatStanzas


def sampleByWindow(opts):
    '''
    Randomly pick windows of stanzas in the book
    (Note that this may pick windows of overlapping chapters)
    '''
    nSamp, winLen = opts['nSamp'], opts['winLen']
    def makeSample(stDict):
        stanzaList = reduceStanzasToList(stDict)
        # keep index of samples
        sampleIndex = []
        # [0 ... dataLength - windowSize]
        dataIndex = range(len(stanzaList) - winLen)

        # go until you have enough samples
        while len(sampleIndex) < nSamp:
            # get diff so that we know which samples haven't been taken
            sampleSet = set(sampleIndex)
            setDiff = [x for x in dataIndex if x not in sampleSet]
            # pick a sample we haven't taken yet
            newIndex = random.choice(setDiff)

            # pick sample + the following stanzas
            newWindow = [newIndex + j for j in range(winLen)]

            # add new samples to main list
            sampleIndex = sampleIndex + newWindow

        # [ indices of samples ] --> [ corresponding stanzas ]
        sampleStanzas = [stanzaList[x] for x in sampleIndex]
        return sampleStanzas
    return makeSample

def numberOfLines(stanzaList):
    # [ stanza ] --> [ number of lines in stanza ]
    stanzaLineCount = map(lambda x: len(x.split('\n')), stanzaList)
    # total of the stanzas
    return sum(stanzaLineCount)

def addWeights(key, stanzaList, denom):
    # weight stanzas by number of lines
    weight = numberOfLines(stanzaList) / float(denom)
    # new object for each book
    return {'book': key, 'stanzas': stanzaList, 'weight':  weight}

def weightBooks(stDict):
    # get total number of lines
    bookLineCount = map(numberOfLines, [stDict[x] for x in stDict.keys()])
    totalLines = sum(bookLineCount)
    # add weights to each book
    booksWithWeights = [addWeights(x, stDict[x], totalLines) for x in stDict]

    return booksWithWeights


def sampleByWeight(opts):
    nSamp = opts['nSamp']
    def makeSample(stDict):
        # get weights
        weightedBooks = weightBooks(stDict)
        # sample based on weight
        #getSampleNo = lambda w: int(nSamp * w)
        def getSampleNo(b):
            samples = int(nSamp * b['weight'])
            pop = len(b['stanzas'])
            return min(samples, pop)

    sampleBooks = map(lambda b: random.sample(b['stanzas'], getSampleNo(b)), weightedBooks)
        # return list of sampled stanzas
        stanzaList = hlp.flattenListOnce(sampleBooks)
        return stanzaList
    return makeSample
