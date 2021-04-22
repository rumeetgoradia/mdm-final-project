import os
import sys
from pathlib import Path

import networkx as nx
import numpy as np
from tqdm import tqdm

from common import check_input_valid, jaccard_similarity, test_correctness
from constants import DIRECTORY
from graph import extract_features, read_graph


def initialize_similarity_matrix(dataset, G, similarity_metric=jaccard_similarity):
    A = nx.adjacency_matrix(G)

    total_P = np.zeros(shape=A.shape[0])
    P = np.zeros(shape=A.shape)
    S = np.zeros(shape=A.shape)

    features = extract_features(dataset)

    for i in tqdm(range(len(features)), desc="Calculating initial similarities"):
        first_node_tags = features[i]
        for j in range(i, len(features)):
            second_node_tags = features[j]
            S[i, j] = S[j, i] = similarity_metric(first_node_tags, second_node_tags)
            P[i, j] = P[j, i] = S[i, j] * A[i, j]
            total_P[i] += P[i, j]
            if i != j:
                total_P[j] += P[j, i]

    return total_P, P, S


def calculate_link_similarity(G, total_P, P, S, c, saved_results_filepath):
    iteration = 1
    difference = 0

    while (iteration == 1 or difference > 0):
        print("Iteration", str(iteration))
        prev_S = S.copy()
        try:
            for a in tqdm(range(S.shape[0])):
                for b in range(a, S.shape[1]):
                    if a == b:
                        S[a, b] = 1
                    else:
                        similarity_transmission = 0
                        for x in G[a]:
                            for y in G[b]:
                                similarity_transmission += prev_S[x, y] * (P[x, a] + P[y, b])
                        denom = G.degree[b] * total_P[a] + G.degree[a] * total_P[b]
                        S[a, b] = S[b, a] = similarity_transmission * c / denom if denom > 0 else 0
            difference = np.sum(abs(np.subtract(prev_S, S)))
            print("Difference:", str(difference))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            np.save(saved_results_filepath, prev_S)
            sys.exit()
        iteration += 1


if __name__ == "__main__":
    dataset = check_input_valid(sys.argv)
    G = read_graph(dataset)
    S = None

    data_directory = os.path.join(DIRECTORY, "similarity_propagation_data", dataset)
    Path(data_directory).mkdir(parents=True, exist_ok=True)
    total_P_path = os.path.join(data_directory, "total_P.npy")
    P_path = os.path.join(data_directory, "P.npy")
    S_path = os.path.join(data_directory, "S.npy")
    most_recent_S_path = os.path.join(data_directory, "most_recent_S.npy")
    results_path = os.path.join(data_directory, "results.npy")

    if not (os.path.exists(results_path)):
        total_P = P = None
        if not (os.path.exists(total_P_path) and
                os.path.exists(P_path) and
                (os.path.exists(S_path) or os.path.exists(most_recent_S_path))):
            total_P, P, S = initialize_similarity_matrix(dataset, G)
            np.save(total_P_path, total_P)
            np.save(P_path, P)
            np.save(S_path, S)
        else:
            total_P = np.load(total_P_path)
            P = np.load(P_path)
            S = np.load(most_recent_S_path) if os.path.exists(most_recent_S_path) else np.load(S_path)

        c = 1
        print("Calculating link similarities:")
        # calculate_link_similarity(G, total_P, P, S, c, most_recent_S_path)
        np.save(results_path, S)
    else:
        print("Loading most recent link similarity results.")
        S = np.load(results_path)

    print(test_correctness(G, S))
    # 0.5162
    # 0.7287 for twitch pr
