from itertools import combinations


colors = list(range(5))


class NotPlanarError(Exception):
    pass


def find_two_nonadjacent(graph, nodes):
    """ Return two vertices from nodes that are not adjacent. """
    for x, y in combinations(nodes, 2):
        if not graph.are_connected(x, y):
            return x, y


def planar_five_color(graph):
    """ Color a planar graph with five colors.

    The output is produced by setting the 'color' attribute of graph.vs to be
    integers between 0 and 4.

    Arguments:
      graph: an igraph Graph object to color.

    Returns:
      the input graph with its 'color' attribute modified.
    """
    n = len(graph.vs)

    if n <= 5:
        graph.vs['color'] = colors[:n]
        return graph

    deg_at_most5_nodes = graph.vs.select(_degree_le=5)
    deg_at_most4_nodes = deg_at_most5_nodes.select(_degree_le=4)
    deg5_nodes = deg_at_most5_nodes.select(_degree_eq=5)

    if not deg5_nodes:
        raise ValueError("Input graph (or recursive subgraph) does not "
            "have a degree 5 node. Input graph is not planar.")

    g_prime = graph.copy()
    # preserved when deleting vertices
    g_prime.vs['old_index'] = list(range(n))

    if len(deg_at_most4_nodes) > 0:
        v = deg_at_most4_nodes[0]
        g_prime.delete_vertices(v.index)
    else:
        v = deg5_nodes[0]
        neighbor_indices = [x['old_index'] for x in g_prime.vs[v.index].neighbors()]

        g_prime.delete_vertices(v.index)
        neighbors_in_g_prime = g_prime.vs.select(old_index_in=neighbor_indices)

        result = find_two_nonadjacent(g_prime, neighbors_in_g_prime)
        if not result:
            raise NotPlanarError("Unable to find two nonadjacent vertices "
                "for recursive call. Input graph is not planar.")

        w1, w2 = result
        merge_two(g_prime, w1, w2)

    colored_g_prime = planar_five_color(g_prime)

    for w in colored_g_prime.vs:
        # subset selection handles the merged w1, w2 with one assignment
        graph.vs[w['old_index']]['color'] = w['color']

    neighbor_colors = set(w['color'] for w in v.neighbors())
    v['color'] = [j for j in colors if j not in neighbor_colors][0]
    return graph


def make_merge_map(G, w1, w2):
    """ Make a list to denote the merging of two vertices.

    The list "maps" the indices of vertices in the unmerged graph to the
    indices of the vertices in the merged graph.

    For example, merging vertices 2 and 4 might consist of the list
    [1, 2, 0, 3, 0, 4, 5] or [0, 1, 2, 3, 2, 4, 5], i.e., index i of the
    list is the "old index" and the value is the new index, but it doesn't
    matter which new indices you choose, just which vertices are mapped to
    the same index.
    """
    n = len(G.vs)
    no_offset = list(range(w2.index))
    offset_part = [w1.index] + [w2.index + j for j in range(n - w2.index - 1)]
    return no_offset + offset_part


def merge_two(graph, w1, w2):
    """ Merge the two input vertices in the input graph.

    Note this mutates the input graph, so the caller is responsible for making a copy.
    """
    merge_map = make_merge_map(graph, w1, w2)
    graph.contract_vertices(merge_map, combine_attrs=(lambda x: x))
