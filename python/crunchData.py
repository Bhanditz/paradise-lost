"""
This module compiles all the data on the text.

It has functions that will make the distance matrix, it organizes all the data,
and exports it in the appropriate fashion.
"""

import itertools as it


def pairGetter(lst):
    """Given a list, return a function that returns a tuple."""
    def getPair(tup):
        return (lst[tup[0]], lst[tup[1]])
    return getPair


def makeDistMatrix(lst, metric):
    """
    Given a list, find distance between all pairs in that list.

    Note that this is quite general, and will work for any list and metric,
    so long as the metric is defined for that list.

    lst fcn --> lst<dict>
    lst fcn --> [ { pair from list, fcn(pair from list) } ]
    """
    # [ tuple(pair of indices in lst) ]
    allPairs = list(it.combinations(range(len(lst)), 2))

    lstPair = pairGetter(lst)
    # [ { pair: tup(i, j), dist: metric(pair) } ]
    distMatrix = [{'pair': p, 'dist': metric(lstPair(p))} for p in allPairs]

    return distMatrix
