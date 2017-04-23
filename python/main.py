import metrics
import samplers
import crunchData
import perseusReader

import os
import json

### --------------------------------------------------- GLOBAL VARIABLES BEGIN

# TODO inlcude options in samplers
SAMPLERS = {
    'windowSample': samplers.sampleByWindow,
    'weightedSample': samplers.sampleByWeight
}

METRICS = {
    'editDistance': metrics.editDistance,
    'jaccardDistance': metrics.jaccardDistance,
    'syllableDistance': metrics.avgSyllableDist,
}

# (sampler key, metric key)
PAIRS = [(sKey, mKey) for sKey in SAMPLERS for mKey in METRICS]

with open('paradise-lost.json', 'r') as popFile:
    POPULATION = json.load(popFile)

### --------------------------------------------------- GLOBAL VARIABLES END


def getPersistenceData(perseusFilePrefix='sample_metric'):
    """
    Assuming a sample has already been taken, uses the metric to calculate:
        matrix = array of pair/distance information
        perseus configuration
        perseus data
    It returns a list with the persistent homology data
    """
    # read in matrix from MATRIX.json
    matrixPath = '{}/matrix.json'.format(perseusFilePrefix)
    with open(matrixPath, 'r') as matrixFile:
        readData = json.load(matrixFile)
    matrix = readData['result']
    # needs number of steps and max dimension
    # matrix, config --> { str(matrix), size of matrix, config.max_dim }
    perseusConfig = crunchData.matrixToPerseusConfig(matrix)

    # write perseus config to INPUT, then run perseus
    inFilename = '{}/input.txt'.format(perseusFilePrefix)
    perseusReader.writePerseusInputFile(perseusConfig, inFilename)
    perseusReader.writePerseusOutput(inFilename, perseusFilePrefix)

    # return persistent homology list
    return perseusReader.compilePerseusOutput(perseusFilePrefix)

# TODO make sure this works
def finalOutput(directory):
    """
    extract data for final export:
        persistenceData,
        sampleStanzas,
        sampleGraph
    """
    # get persistence data <list>
    persistenceData = getPersistenceData(directory)

    # get sample <list>
    samplePath = '{}/sample.json'.format(directory)
    with open(samplePath, 'r') as sampleFile:
        readSample = json.load(sampleFile)
    sampleStanzas = readSample

    # TODO put in graph functionality
    # put them all in one object
    dataJSON = {
        'persistenceData': persistenceData,
        'sampleStanzas': sampleStanzas
    }

    return dataJSON


def makeSample(pop, sampler, opts, directory):
    """Get the sample, write to file, return sample data"""
    sampleData = sampler(opts)(pop)
    # write samples to file
    samplePath = '{}/sample.json'.format(directory)
    with open(samplePath, 'w') as sampleFile:
        json.dump(sampleData, sampleFile)
    # return sample
    return sampleData

def makeMatrix(sampleData, metric, directory):
    """calculate distribution matrix given a metric and sample data"""
    # calculate sample and matrix
    matrix = crunchData.makeDistMatrix(sampleData, metric)
    # write matrix to file
    matrixPath = '{}/matrix.json'.format(directory)
    with open(matrixPath, 'w') as matrixFile:
        json.dump(matrix, matrixFile)
