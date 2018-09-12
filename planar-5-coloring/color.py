from itertools import combinations


def make_merge_map(G, w1, w2):
    ''' Make a list to denote the merging of two vertices the list "maps" the indices
    of vertices in the unmerged graph to the indices of the vertices in the merged
    graph.  For example, merging vertices 2 and 4 might consist of the list
    [1,2,0,3,0,4,5] or [0,1,2,3,2,4,5], i.e. index i of the list is the "old index"
    and the value is the new index, but it doesn't matter which new indices you
    choose, just which vertices are mapped to the same index.
    '''
    n = len(G.vs)
    no_offset = list(range(w2.index))
    offset_part = [w1.index] + [w2.index + j for j in range(n - w2.index - 1)]

    return no_offset + offset_part


def merge_two(G, w1, w2):
    # merge two vertices by constructing a merge map for igraph's
    # contract_vertices function
    merge_map = make_merge_map(G, w1, w2)
    G.contract_vertices(merge_map, combine_attrs=(lambda x: x))


def find_two_nonadjacent(G, nodes):
    for x, y in combinations(nodes, 2):
        if not G.are_connected(x, y):
            return x, y


colors = list(range(5))


def planar_five_color(G):
    # Color a planar graph with five colors by setting the 'color'
    # attribute of the nodes of the input graph.
    # planarFiveColor: Graph -> Graph
    n = len(G.vs)

    if n <= 5:
        G.vs['color'] = colors[:n]
        return G

    deg_at_most5_nodes = G.vs.select(_degree_le=5)
    deg_at_most4_nodes = deg_at_most5_nodes.select(_degree_le=4)
    deg5_nodes = deg_at_most5_nodes.select(_degree_eq=5)

    g_prime = G.copy()
    g_prime.vs['old_index'] = list(range(n))  # preserved when deleting vertices

    if len(deg_at_most4_nodes) > 0:
        v = deg_at_most4_nodes[0]
        g_prime.delete_vertices(v.index)
    else:
        v = deg5_nodes[0]
        nbr_indices = [x['old_index'] for x in g_prime.vs[v.index].neighbors()]

        g_prime.delete_vertices(v.index)
        neighbors_in_g_prime = g_prime.vs.select(old_index_in=nbr_indices)

        w1, w2 = find_two_nonadjacent(g_prime, neighbors_in_g_prime)
        merge_two(g_prime, w1, w2)

    colored_g_prime = planar_five_color(g_prime)

    for w in colored_g_prime.vs:
        # subset selection handles the merged w1, w2
        G.vs[w['old_index']]['color'] = w['color']

    neighbor_colors = set(w['color'] for w in v.neighbors())
    v['color'] = [j for j in colors if j not in neighbor_colors][0]

    return G
