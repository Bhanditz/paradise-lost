import re
import os
import helpers as hlp
import json

def writePerseusInputFile(config, filename):
    c = config
    perseusFileString = '{}\n{} {} {} {}\n{}'.format(c['size'], c['start'], c['step_size'], c['no_steps'], c['max_dim'], c['matrix'])
    with open(filename, 'w') as outFile:
        outFile.write(perseusFileString)

def writePerseusOutput(inFilename, prefix):
    shellCommand = '../perseusMac distmat {} {}/output'.format(inFilename, prefix)
    os.system(shellCommand)

def parsePerseusString(str):
    """convert 'num num'-->[num num]"""
    return map(int, str.split(" "))


def convertOutputFile(path):
    """Convert perseus output_n.txt to array"""

    # read in file
    with open(path, 'r') as persFile:
        perStr = persFile.read()

    # find the dimension of the complexes
    dim = int(re.search(r'\d+', path).group())

    # split on linebreaks
    perLst = filter(lambda x: x != '', perStr.split('\n'))

    if perLst:
        # [ 'num num' ] --> [ [num, num] ]
        perParsed= map(parsePerseusString, perLst)
        # [ [birth death] ] --> [ {generator, dimension, birth, death} ]
        perData = [ {"gen": g[0], "dim": dim, "birth": g[1][0], "death": g[1][1]} for g in enumerate(perParsed)]
    else:
        # return identifier if file is empty
        perData = "NO_GENERATORS"

    return perData


def compilePerseusOutput(directory):
    """Extract persistence data from all perseus output files in a directory"""

    # directory --> [ output_i.txt ]
    outputFilter = lambda f: bool(re.match('output_\d\.txt', f))
    outputFiles = filter(outputFilter, os.listdir(directory))
    outputPaths = map(lambda f: '{}/{}'.format(directory, f), outputFiles)
    # [ output_i.txt ] --> [ [homology data i] ]
    outputData = map(convertOutputFile, outputPaths)
    persData = filter(lambda r: r != "NO_GENERATORS", outputData)

    # [ [homology data i] ] --> [ flat homology data ]
    flatData = hlp.flattenListOnce(persData)

    # remove empty homologies
    # [ {generator, dimension, birth, death} ]
    return flatData
