import metrics
import crunchData
import graphMaker

def test_stanzaLen_metric():
    inputs = (
        'the cat saw the dog',
        'the dog saw the fish',
    )
    assert metrics.stanzaLen(inputs) == 1

def test_edit_distance_metric():
    inputs = (
        'the cat saw the dog',
        'the dog saw the fish',
    )
    assert metrics.editDistance(inputs) == 7

def test_make_distance_matrix():
    inputs = [
        'the cat saw the dog',
        'the dog saw the fish',
        'the cat saw the fish'
    ]

    output = [
        {'pair': (0, 1), 'dist': 7},
        {'pair': (0, 2), 'dist': 4},
        {'pair': (1, 2), 'dist': 3}
    ]

    assert crunchData.makeDistMatrix(inputs, metrics.editDistance) == output

def test_filter_by_epsilon():
    inputPairs = [{'pair': (1, 2), 'dist': 2}, {'pair': (3, 5), 'dist': 6}]
    inputEps = 4
    output = [(1, 2)]
    assert graphMaker.filterByEpsilon(inputPairs, inputEps) == output

def test_make_graph():
    inputPairs = [
                {'pair': (1, 2), 'dist': 2},
                {'pair': (3, 5), 'dist': 6},
                {'pair': (2, 5), 'dist': 1}
                ]
    inputEps = 3
    output = { '1': { '2': {}}, '3': {}, '5': {'2': {}}, '2': { '1': {}, '5': {}}}

    assert graphMaker.makeEpsGraph(inputPairs, inputEps) == output
