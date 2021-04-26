import os
import sys
from pathlib import Path

import numpy as np
from tqdm import tqdm

from common import check_input_valid, jaccard_similarity, test_correctness
from constants import DIRECTORY
from graph import read_graph


def fill_similarity_matrix(G):
    num_nodes = G.number_of_nodes()
    S = np.zeros(shape=(num_nodes, num_nodes))

    for i in tqdm(range(num_nodes), desc="Calculating similarities"):
        first_node_edges = set(G[i])
        for j in range(i, num_nodes):
            second_node_edges = set(G[j])
            S[i, j] = S[j, i] = jaccard_similarity(first_node_edges, second_node_edges)

    return S


if __name__ == "__main__":
    dataset = check_input_valid(sys.argv)
    G = read_graph(dataset)

    data_directory = os.path.join(DIRECTORY, "edge_similarity_data", dataset)
    Path(data_directory).mkdir(parents=True, exist_ok=True)
    results_path = os.path.join(data_directory, "results.npy")

    if os.path.exists(results_path):
        S = np.load(results_path)
    else:
        S = fill_similarity_matrix(G)
        np.save(results_path, S)

    print(test_correctness(G, S))
