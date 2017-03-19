'''
This module loads in Paradise Lost as a .txt file from
Project Gutenberg.  It also parses it and stores it in
JSON format, with stanzas organized by book
'''

import urllib2
import json
import helpers as hp

def readFromURL(URL, outFile):
    wholeText = urllib2.urlopen(URL).read()
    with open(outFile, 'w') as f:
        f.write(wholeText)

def parseToJSON(txtFile, jsonFile):
    with open(txtFile, 'r') as inFile:
        wholeText = inFile.read()

    firstLine = 'scanner\)\s*'
    lastLine = '\s*(End of the Project)'

    # get only the section we care about
    truncatedText = hp.getWindow(wholeText, firstLine, lastLine)

    # separate text by book
    bookSplitExpr = '(THE END[\.\s*](OF THE \w* \w*.))?'
    bookList = hp.textSplitter(truncatedText, bookSplitExpr)[::3]

    # break up stanzas in each book
    bookTuples = [ hp.splitStanzas(x[0], x[1]) for x in enumerate(bookList)]

    # create dict { bookN: [ Stanzas ] }
    bookDict = { x[0]: x[1] for x in bookTuples }

    # write dict to json
    with open(jsonFile, 'w') as outFile:
        json.dump(bookDict, outFile)



# This will run when you run loadFile.py in the command line

URL = 'http://www.gutenberg.org/cache/epub/20/pg20.txt'
textFile = 'paradise-lost.txt'
jsonFile = 'paradise-lost.json'

# uncomment if you want to read from URL
#readFromURL(URL, textFile)

parseToJSON(textFile, jsonFile)
