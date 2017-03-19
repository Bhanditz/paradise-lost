"""
This module contains metrics and helpers for those metrics.

All metrics will take in a pair (x, y) and return a non-negative real number.
"""

from nltk.metrics import edit_distance

def editDistance(pair):
    return edit_distance(pair[0], pair[1])

def stanzaLen(pair):
    # TODO This is not a metric... strings of the same length map to zero,
    # but are not the same element
    return abs(len(pair[0]) - len(pair[1]))
