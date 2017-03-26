"""
Holds functionality for any graphs we might create.
"""

import networkx as nx
import matplotlib.pyplot as plt
from helpers import getNodes

def filterByEpsilon(lst, eps):
    r"""
    Filter out all pairs that have value less than epsilon.

    lst float --> lst
    [ {pair, dist} ] eps --> [ {pairs | dist < eps } ]
    """
    return map(lambda x: x['pair'], filter(
        lambda y: y['dist'] < eps, lst
    ))


def makeEpsGraph(lst, eps):
    r"""
    Make graph from list of pairs

    lst --> dict
    [ (i,j) ] --> nx.Graph( [(i, j)] )
    """
    nodes = [str(x) for x in getNodes(lst)]
    epsList = filterByEpsilon(lst, eps)
    edgeList = [ ( str(x[0]), str(x[1]) ) for x in epsList]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edgeList)

    return G.adj
