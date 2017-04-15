"""
This module offers some helper functions for the
non-computational aspects of this project.  For example,
it has functions that use regular expressions to parse
the text---not particularly interesting, topologically
"""

import re  # regular expression library
import json
import itertools


def getWindow(text, first, last):
    """
    Return text in a specified window.

    Given a string and two regular expressions, return
    only the part of the text between the first instance of
    those expressions.  If nothing is found, return the original
    text.

    str regex regex --> list<str>
    text first last --> [ text.find(first) ... text.find(last) ]
    """
    left = re.search(first, text)
    right = re.search(last, text)

    if (not left) and (not right):
        print 'No match was found'
        return text
    elif (left) and (not right):
        print 'No right match was found'
        return text[left.end():]
    elif (not left) and (right):
        print 'No left match was found'
        return text[:right.start()]
    else:
        return text[left.end(): right.start()]


def textSplitter(text, splitExp):
    """
    Split the text and filer out empty lines.

    str regex --> lst
    text regex --> text.split(regex)
    """
    textSplit = re.split(splitExp, text)
    return filter(lambda x: x != '', textSplit)


def splitStanzas(index, book):
    r"""
    Split a book into stanzas.

    int str --> tup( str, lst<str>)
    index text --> ( index, text.split(\n\n) )
    """
    # key is bookN
    key = 'book{}'.format(index + 1)

    # find window between start and end of bookN
    firstLine = '(BOOK\s*[IVX]+\.?\s*)'
    lastLine = 'GO_UNTIL_END' if index < 9 else '(\s*(THE END\.))'
    stanzaWindow = getWindow(book, firstLine, lastLine)

    # string --> [ stanzas ]
    stanzaSplitExp = '\s(\r\n)\s*'
    stanzas = textSplitter(stanzaWindow, stanzaSplitExp)[::2]

    # tuple( str(bookN), str_list(stanzas) )
    return (key, stanzas)


def flattenListOnce(lst):
    return list(itertools.chain(*lst))


def getNodes(lst):
    """Get unique nodes from list of data"""
    pairs = [ [x['pair'][0], x['pair'][1]] for x in lst]
    items = list(itertools.chain.from_iterable(pairs))
    return list(set(items))

def getStepStats(arr, no_steps=100):
    """Get stats for persistent homology calculation"""
    distances = map(lambda x: x['dist'], arr)
    minD, maxD = min(distances), max(distances)

    step_size = (maxD - minD) / float(no_steps)

    return {"start": max(minD-1, 0), "step_size": step_size, "no_steps": no_steps}


def updateArrayEntry(arr, datum, upperRight=True):
    pair = datum['pair']
    row = pair[0] if upperRight else pair[1]
    col = pair[1] if upperRight else pair[0]

    arr[row][col] = datum['dist']
    # no return, update in place


def writeToJSON(jsonData, inFile):
    """Import a dict to json file."""
    with open(inFile, 'w') as f:
        json.dump(f, jsonData)


def readJSON(readFile):
    """Read JSON to dict."""
    with open(readFile, 'r') as f:
        data = json.read(f)
    return data
