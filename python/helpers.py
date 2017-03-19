"""
This module offers some helper functions for the
non-computational aspects of this project.  For example,
it has functions that use regular expressions to parse
the text---not particularly interesting, topologically
"""

import re # regular expression library

def getWindow(text, first, last):
    """
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
        return text[left.end() : right.start()]

def textSplitter(text, splitExp):
    """
    Split the text and filer out empty lines

    str regex --> lst
    text regex --> text.split(regex)
    """
    textSplit = re.split(splitExp, text)
    return filter(lambda x: x != '', textSplit)

def splitStanzas(index, book):
    """
    Split a book into stanzas
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
