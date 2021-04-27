import os
import sys
from pathlib import Path

import networkx as nx
import numpy as np
from tqdm import tqdm

from common import check_input_valid, jaccard_similarity, test_correctness
from community_detection import read_communities
from constants import DIRECTORY
from graph import extract_features, read_graph
from similarity_propagation import calculate_link_similarity


def initialize_similarity_matrix(dataset, G, communities):
    A = nx.adjacency_matrix(G)

    total_P = np.zeros(shape=A.shape[0])
    P = np.zeros(shape=A.shape)
    S = np.zeros(shape=A.shape)

    features = extract_features(dataset)

    for i in tqdm(range(len(features)), desc="Calculating initial similarities"):
        first_node_features = features[i]
        first_node_edges = set(G[i])
        for j in range(i, len(features)):
            if communities[i] != communities[j]:
                second_node_features = features[j]
                S[i, j] = S[j, i] = jaccard_similarity(first_node_features, second_node_features)
            else:
                second_node_edges = set(G[j])
                S[i, j] = S[j, i] = jaccard_similarity(first_node_edges, second_node_edges)
            P[i, j] = P[j, i] = S[i, j] * A[i, j]
            total_P[i] += P[i, j]
            if i != j:
                total_P[j] += P[j, i]

    return total_P, P, S


def fill_similarity_matrix(G, communities, total_P, P, S, saved_results_filepath):
    iteration = 1
    difference = 0

    while (iteration == 1 or difference > 0):
        print("Iteration", str(iteration))
        prev_S = S.copy()
        try:
            for a in tqdm(range(S.shape[0])):
                for b in range(a, S.shape[1]):
                    if (a == b):
                        S[a, b] = 1
                    elif (communities[a] != communities[b]):
                        calculate_link_similarity(G, S, prev_S, P, total_P, a, b)
            difference = np.sum(abs(np.subtract(prev_S, S)))
            print("Difference:", str(difference))
        except:
            print("Saving most recent similarity matrix and stopping calculations.")
            np.save(saved_results_filepath, prev_S)
            return
            # sys.exit()
        iteration += 1


if __name__ == "__main__":
    dataset = check_input_valid(sys.argv)
    G = read_graph(dataset)
    communities = read_communities(dataset)
    S = None

    data_directory = os.path.join(DIRECTORY, "dynamic_link_prediction_data", dataset)
    Path(data_directory).mkdir(parents=True, exist_ok=True)
    total_P_path = os.path.join(data_directory, "total_P.npy")
    P_path = os.path.join(data_directory, "P.npy")
    S_path = os.path.join(data_directory, "S.npy")
    most_recent_S_path = os.path.join(data_directory, "most_recent_S.npy")
    results_path = os.path.join(data_directory, "results.npy")
    score_path = os.path.join(data_directory, "score.txt")

    if not (os.path.exists(results_path)):
        total_P = P = None
        if not (os.path.exists(total_P_path) and
                os.path.exists(P_path) and
                (os.path.exists(S_path) or os.path.exists(most_recent_S_path))):
            total_P, P, S = initialize_similarity_matrix(dataset, G, communities)
            np.save(total_P_path, total_P)
            np.save(P_path, P)
            np.save(S_path, S)
        else:
            total_P = np.load(total_P_path)
            P = np.load(P_path)
            S = np.load(most_recent_S_path) if os.path.exists(most_recent_S_path) else np.load(S_path)

        print("Calculating link similarities:")
        fill_similarity_matrix(G, communities, total_P, P, S, most_recent_S_path)
        np.save(results_path, S)
    else:
        print("Loading most recent link similarity results.")
        S = np.load(results_path)

    with open(score_path, "w") as score_file:
        score = test_correctness(G, S)
        print(score)
        score_file.write(str(score))
