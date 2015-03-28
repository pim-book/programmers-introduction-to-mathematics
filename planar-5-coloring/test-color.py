import igraph
from color import planarFiveColor
from color import makeMergeMap

from unittest import test


def improperlyColored(G, e):
    return G.vs[e.source]['color'] == G.vs[e.target]['color']


def properlyColored(G):
    return 0 == sum(1 for e in G.es if improperlyColored(G, e))


def test5Exactly():
    G = igraph.Graph(n=5)
    planarFiveColor(G)

    test([0, 1, 2, 3, 4], G.vs['color'])


def testLessThan5():
    G = igraph.Graph(n=3)
    planarFiveColor(G)

    test([0, 1, 2], G.vs['color'])


def testHasDegree4Node():
    G = igraph.Graph.Full(n=6)
    G.delete_edges([(0, 1)])
    test(4, G.degree(0))

    planarFiveColor(G)

    test(True, properlyColored(G))


def testMergeMap():
    G = igraph.Graph.Full(n=6)
    w1 = G.vs[1]
    w2 = G.vs[3]

    actual = makeMergeMap(G, w1, w2)
    test([0, 1, 2, 1, 3, 4], actual)


def testAllDegree5():
    G = igraph.Graph(n=12)
    flower = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
              (1, 2), (1, 5), (1, 6), (1, 7),
              (2, 3), (2, 7), (2, 8),
              (3, 4), (3, 8), (3, 9),
              (4, 5), (4, 9), (4, 10),
              (5, 6), (5, 10),
              (6, 7), (6, 10), (6, 11),
              (7, 8), (7, 11),
              (8, 9), (8, 11),
              (9, 10), (9, 11),
              (10, 11)]

    G.add_edges(flower)
    planarFiveColor(G)

    test(True, properlyColored(G))


if __name__ == "__main__":
    tests = [name for name in dir() if len(name) > 4 and name[:4] == 'test']
    for name in tests:
        eval('%s()' % name)
