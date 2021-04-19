import random


def test_correctness(G, S, n=5000):
    edges = G.edges()
    non_edges = set()
    for i in range(G.number_of_nodes() - 1):
        for j in range(i + 1, G.number_of_nodes()):
            non_edges.add((i, j))
            non_edges.add((j, i))
    non_edges -= set(edges)
    non_edges = list(non_edges)

    len_edges = len(edges)
    len_non_edges = len(non_edges)
    success_count = 0
    tie_count = 0
    for i in range(n):
        edge = edges[random.randrange(len_edges)]
        non_edge = non_edges[random.randrange(len_non_edges)]

        if (S[edge[0], edge[1]] > S[non_edge[0], non_edge[1]]):
            success_count += 1
        elif (S[edge[0], edge[1]] == S[non_edge[0], non_edge[1]]):
            tie_count += 1

    return (success_count + 0.5 * tie_count) / n
