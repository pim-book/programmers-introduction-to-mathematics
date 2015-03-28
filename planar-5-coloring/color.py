from itertools import combinations


def makeMergeMap(G, w1, w2):
    '''
      Make a list to denote the merging of two vertices the list "maps" the indices
    of vertices in the unmerged graph to the indices of the vertices in the merged
    graph.  For example, merging vertices 2 and 4 might consist of the list
    [1,2,0,3,0,4,5] or [0,1,2,3,2,4,5], i.e. index i of the list is the "old index"
    and the value is the new index, but it doesn't matter which new indices you
    choose, just which vertices are mapped to the same index.
    '''
    n = len(G.vs)
    noOffset = list(range(w2.index))
    offsetPart = [w1.index] + [w2.index + j for j in range(n - w2.index - 1)]

    return noOffset + offsetPart


def mergeTwo(G, w1, w2):
    # merge two vertices by constructing a merge map for igraph's
    # contract_vertices function
    mergeMap = makeMergeMap(G, w1, w2)
    G.contract_vertices(mergeMap, combine_attrs=(lambda x: x))


def findTwoNonadjacent(G, nodes):
    for x, y in combinations(nodes, 2):
        if not G.are_connected(x, y):
            return x, y


colors = list(range(5))


def planarFiveColor(G):
    # Color a planar graph with five colors by setting the 'color'
    # attribute of the nodes of the input graph.
    # planarFiveColor: Graph -> Graph
    n = len(G.vs)

    if n <= 5:
        G.vs['color'] = colors[:n]
        return G

    degAtMost5Nodes = G.vs.select(_degree_le=5)
    degAtMost4Nodes = degAtMost5Nodes.select(_degree_le=4)
    deg5Nodes = degAtMost5Nodes.select(_degree_eq=5)

    GPrime = G.copy()
    GPrime.vs['oldIndex'] = list(range(n))  # preserved when deleting vertices

    if len(degAtMost4Nodes) > 0:
        v = degAtMost4Nodes[0]
        GPrime.delete_vertices(v.index)
    else:
        v = deg5Nodes[0]
        nbrIndices = [x['oldIndex'] for x in GPrime.vs[v.index].neighbors()]

        GPrime.delete_vertices(v.index)
        neighborsInGPrime = GPrime.vs.select(oldIndex_in=nbrIndices)

        w1, w2 = findTwoNonadjacent(GPrime, neighborsInGPrime)
        mergeTwo(GPrime, w1, w2)

    coloredGPrime = planarFiveColor(GPrime)

    for w in coloredGPrime.vs:
        # subset selection handles the merged w1, w2
        G.vs[w['oldIndex']]['color'] = w['color']

    neighborColors = set(w['color'] for w in v.neighbors())
    v['color'] = [j for j in colors if j not in neighborColors][0]

    return G
