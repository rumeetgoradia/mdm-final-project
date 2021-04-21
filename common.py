import random

import networkx as nx
import numpy as np
from tqdm import tqdm


def test_correctness(G, S, n=5000):
    A = nx.adjacency_matrix(G)
    non_A = np.ones(shape=(G.number_of_nodes(), G.number_of_nodes())) - A

    edges = list(G.edges())
    non_edges = []
    for i in tqdm(range(G.number_of_nodes() - 1), desc="Finding non-edges for correctness test"):
        for j in range(i + 1, G.number_of_nodes()):
            if (non_A[i, j] == 1):
                non_edges.append((i, j))
                non_edges.append((j, i))

    len_edges = len(edges)
    len_non_edges = len(non_edges)
    success_count = 0
    tie_count = 0
    for i in tqdm(range(n), desc="Testing correctness"):
        edge = edges[random.randrange(0, len_edges)]
        non_edge = non_edges[random.randrange(0, len_non_edges)]

        if (S[edge[0], edge[1]] > S[non_edge[0], non_edge[1]]):
            success_count += 1
        elif (S[edge[0], edge[1]] == S[non_edge[0], non_edge[1]]):
            tie_count += 1

    return (success_count + 0.5 * tie_count) / n
