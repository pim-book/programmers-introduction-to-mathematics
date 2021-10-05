from assertpy import assert_that
import igraph
import pytest

from color import NotPlanarError
from color import make_merge_map
from color import planar_five_color


def improperly_colored(G, e):
    return G.vs[e.source]['color'] == G.vs[e.target]['color']


def properly_colored(G):
    return 0 == sum(1 for e in G.es if improperly_colored(G, e))


def test_five_node_empty_graph():
    G = igraph.Graph(n=5)
    planar_five_color(G)
    assert_that(G.vs['color']).is_equal_to([0, 1, 2, 3, 4])


def test_three_node_empty_graph():
    G = igraph.Graph(n=3)
    planar_five_color(G)
    assert_that(G.vs['color']).is_equal_to([0, 1, 2])


def test_color_with_degree_four_node():
    G = igraph.Graph.Full(n=6)
    G.delete_edges([(0, 1)])
    assert_that(G.degree(0)).is_equal_to(4)

    planar_five_color(G)
    assert_that(properly_colored(G)).is_true()


def test_merge_map():
    G = igraph.Graph.Full(n=6)
    w1 = G.vs[1]
    w2 = G.vs[3]
    actual_merged_map = make_merge_map(G, w1, w2)
    assert_that(actual_merged_map).is_equal_to([0, 1, 2, 1, 3, 4])


def test_color_five_regular_planar_graph():
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
    planar_five_color(G)
    assert_that(properly_colored(G)).is_true()


def test_failure_of_deg_5_node():
    G = igraph.Graph.Full(n=7)
    with pytest.raises(ValueError):
        planar_five_color(G)


def test_failure_of_recursive_call():
    G = igraph.Graph.Full(n=7)
    G.delete_edges([(0, 1)])  # leaves node 0 with deg 5
    with pytest.raises(NotPlanarError):
        planar_five_color(G)
