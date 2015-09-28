# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/generic.py -- Generic cascading detection tools.
from .loader import LoadNumberFile, SaveSortedList
from sortedcontainers import SortedList
from itertools import combinations

def SparsifyEdgeList(edgeListPath, clustersPath):
    '''
        Return a edge list that do not include the edges that
        are present in a clusters file (of edges).
    '''
    # Load the edge list and clusters as a *sorted* list of lists of tuples
    edgeList = LoadNumberFile(edgeListPath)
    clusters = LoadNumberFile(clustersPath)

    # Return the edge list minus assigned edges
    for edgeCommunity in clusters:
        for edge in edgeCommunity:
            try:
                edgeList.remove([edge])
            except ValueError:
                pass

    return edgeList


def ToEdgeClusters(edgeListPath, clustersPath):
    '''
        Convert a node clusters file to an edge clusters path.
    '''
    # Load the edge list and clusters as a *sorted* list of lists of tuples
    edgeList = LoadNumberFile(edgeListPath)
    edgeClusters = SortedList()
    with open(clustersPath, 'r') as f:
        for l in f:
            nodes = [int(x) for x in l.strip().split()]
            cluster = SortedList()
            for e in combinations(sorted(nodes), 2):
                if edgeList.count([e]) is not 0:
                    cluster.add(e)
            edgeClusters.add(cluster)
    with open(clustersPath, 'w') as f:
        for c in edgeClusters:
            for t in c:
                f.write(str(t[0]) + " " + str(t[1]) + " ")
            f.write("\n")



def PurgeClusters(clustersPath, minSize):
    '''
        Remove communities that contain less edges than minSize
    '''
    clusters = LoadNumberFile(clustersPath)
    clusters = SortedList(x for x in clusters if len(x) >= minSize)
    SaveSortedList(clusters, clustersPath)

