import metrics
import crunchData

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
