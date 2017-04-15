# This is just an outline.  This code currently does not run.

# reference for samplers
SAMPLERS = {'random': randomSample()}

# reference for metrics
METRICS = {'edit': editDistance()}

# should have a proper data structre in place after sampling
for sample in SAMPLES.keys():
    for metric in METRICS.keys():
        directory = 'homology/{}_{}'.format(sample, metric) #UNDEFINED
        # get perseus config for sample + metric pair
        # store config info
        # do perseus executable--needs config and a distance matrix
        # compile and store perseus outputs

# convert to json
