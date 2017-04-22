import metrics
import samplers
import crunchData
import perseusReader

import os
import json

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

def writeMetricData(perseusFilePrefix='sample_metric'):
    """
    Assuming a sample has already been taken, uses the metric to calculate:
        matrix = array of pair/distance information
        perseus configuration
        perseus data
    It returns an object with the data
    """
    # read in matrix from MATRIX.json
    matrixPath = '{}/MATRIX.json'.format(perseusFilePrefix)
    with open(matrixPath, 'r') as matrixFile:
        readData = json.load(matrixFile)
    matrix = readData['result']
    # needs number of steps and max dimension
    # matrix, config --> { str(matrix), size of matrix, config.max_dim }
    perseusConfig = crunchData.matrixToPerseusConfig(matrix)

    # write perseus config to INPUT, then run perseus
    inFilename = '{}/INPUT.txt'.format(perseusFilePrefix)
    perseusReader.writePerseusInputFile(perseusConfig, inFilename)
    perseusReader.writePerseusOutput(inFilename, perseusFilePrefix)
