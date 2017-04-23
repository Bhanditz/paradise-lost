import metrics
import samplers
import crunchData
import perseusReader
import helpers as hlp

import os
import json

### --------------------------------------------------- GLOBAL VARIABLES BEGIN

# TODO inlcude options in samplers
SAMPLE_NUMBER = 214

SAMPLERS = {
    'windowSample': {
        'fcn': samplers.sampleByWindow,
        'opts': { 'nSamp': SAMPLE_NUMBER, 'winLen': 4}
    },
    'weightedSample': {
        'fcn': samplers.sampleByWeight,
        'opts': { 'nSamp': SAMPLE_NUMBER }
    }
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


def getPersistenceData(directory):
    """
    Assuming a sample has already been taken, uses the metric to calculate:
        matrix = array of pair/distance information
        perseus configuration
        perseus data
    It returns a list with the persistent homology data
    """
    # read in matrix from MATRIX.json
    matrixPath = '{}/matrix.json'.format(directory)
    with open(matrixPath, 'r') as matrixFile:
        readData = json.load(matrixFile)
    matrix = readData
    # needs number of steps and max dimension
    # matrix, config --> { str(matrix), size of matrix, config.max_dim }
    perseusConfig = crunchData.matrixToPerseusConfig(matrix)

    # write perseus config to INPUT, then run perseus
    inFilename = '{}/input.txt'.format(directory)
    perseusReader.writePerseusInputFile(perseusConfig, inFilename)
    perseusReader.writePerseusOutput(inFilename, directory)

    # return persistent homology list
    return perseusReader.compilePerseusOutput(directory)

# TODO make sure this works
def finalOutput(samplerKey, metricKey, prefix='perseusData/test'):
    """
    extract data for final export:
        persistenceData,
        sampleStanzas,
        sampleGraph
    """

    directory = '{}/{}/{}'.format(prefix, samplerKey, metricKey)
    # get persistence data <list>
    persistenceData = getPersistenceData(directory)

    # get sample <list>
    samplePath = '{}/{}/sample.json'.format(prefix, samplerKey)
    with open(samplePath, 'r') as sampleFile:
        sampleStanzas = json.load(sampleFile)

    # get matrix <list>
    matrixPath = '{}/{}/{}/matrix.json'.format(prefix, samplerKey, metricKey)
    with open(matrixPath, 'r') as matrixFile:
        distMatrix = json.load(matrixFile)

    # TODO put in graph functionality
    # put them all in one object
    dataJSON = {
        'persistenceData': persistenceData,
        'sampleStanzas': sampleStanzas,
        'matrix': distMatrix
    }

    # write data to index.json
    indexPath = '{}/index.json'.format(directory)
    with open(indexPath, 'w') as indexFile:
        json.dump(dataJSON, indexFile)

    return dataJSON


def makeSample(pop, sampler, opts, directory):
    """Get the sample, write to file, return sample data"""
    sampleData = sampler(opts)(pop)
    # write samples to file
    samplePath = '{}/sample.json'.format(directory)
    with open(samplePath, 'w') as sampleFile:
        json.dump(sampleData, sampleFile)
    # return sample
    print '     sample written to: {}'.format(samplePath)
    return sampleData


def makeMatrix(sampleData, metric, directory):
    """calculate distribution matrix given a metric and sample data"""
    # calculate sample and matrix
    matrix = crunchData.makeDistMatrix(sampleData, metric)
    # write matrix to file
    matrixPath = '{}/matrix.json'.format(directory)
    with open(matrixPath, 'w') as matrixFile:
        json.dump(matrix, matrixFile)
    print '     matrix written to: {}'.format(matrixPath)

def runSingleSampleComputation(pop, samplerKey, metricKey, directory):
    """collect sample and calculate ditribution matrix"""
    samplerFcn, samplerOpts = SAMPLERS[samplerKey]['fcn'], SAMPLERS[samplerKey]['opts']
    metricFcn = METRICS[metricKey]
    # get sample and write to file
    samplePath = '{}/{}'.format(directory, samplerKey)
    sampleData = makeSample(pop, samplerFcn, samplerOpts, samplePath)
    # write matrix to file
    matrixPath = '{}/{}/{}'.format(directory, samplerKey, metricKey)
    makeMatrix(sampleData, metricFcn, matrixPath)


def sampleThenPerseus(pop, samplerKey, metricKey, directory):
    # write sample + matrix to file, return path to matrix
    runSingleSampleComputation(pop, samplerKey, metricKey, directory)
    # output data
    allData = finalOutput(samplerKey, metricKey)

def sampleAll(outputDir):
    for samplerKey in SAMPLERS:
        print 'current sampler: {}'.format(samplerKey)
        samplerFcn, samplerOpts = SAMPLERS[samplerKey]['fcn'], SAMPLERS[samplerKey]['opts']
        samplerPath = '{}/{}'.format(outputDir, samplerKey)
        sampleData = makeSample(POPULATION, samplerFcn, samplerOpts, samplerPath)
        for metricKey in METRICS:
            print '     current metric: {}'.format(metricKey)
            metricFcn = METRICS[metricKey]
            matrixPath = '{}/{}/{}'.format(outputDir, samplerKey, metricKey)
            print '     loading matrix...'
            makeMatrix(sampleData, metricFcn, matrixPath)
            print '     matrix loaded!'
            finalOutput(samplerKey, metricKey)
            print '     perseus loaded!'


def compileJSON(outputDir):
    JSON = dict()
    # compile master JSON
    for samplerKey in SAMPLERS:
        JSON[samplerKey] = dict()
        for metricKey in METRICS:
            jsonPath = '{}/{}/{}/index.json'.format(outputDir, samplerKey, metricKey)
            JSON[samplerKey][metricKey] = hlp.readJSON(jsonPath)
    # write to file
    outputFile = '{}/index.json'.format(outputDir)
    hlp.writeToJSON(JSON, outputFile)
