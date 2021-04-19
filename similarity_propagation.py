import sys
from math import sqrt
from os import makedirs, path, sep

import networkx as nx
import numpy as np
from tqdm import tqdm

from common import test_correctness
from graph import read_graph


def generate_tag_set(line: str):
    tags = set()
    split_line = line.split(" ")
    if len(split_line) > 1:
        for i in range(1, int(split_line[0]) + 1):
            tags.add(int(split_line[i]))
    return tags


def cosine_similarity(tags1: set, tags2: set):
    return len(tags1.intersection(tags2)) / (sqrt(len(tags1)) * sqrt(len(tags2))) if (sqrt(len(tags1)) * sqrt(len(tags2))) > 0 else 0


def jaccard_similarity(tags1: set, tags2: set):
    return len(tags1.intersection(tags2)) / len(tags1.union(tags2)) if len(tags1.union(tags2)) > 0 else 0


def initialize_similarity_matrix(G, similarity_metric=jaccard_similarity):
    A = nx.adjacency_matrix(G)
    # E = G.edges()
    total_P = np.zeros(shape=A.shape[0])
    P = np.zeros(shape=A.shape)
    S = np.zeros(shape=A.shape)

    tags = {}
    tags_file = open('./data/item-tag.dat')
    for i, line in enumerate(tags_file):
        tags[i] = generate_tag_set(line)
    tags_file.close()

    for i in tqdm(range(len(tags))):
        first_node_tags = tags[i]
        for j in range(i, len(tags)):
            second_node_tags = tags[j]
            S[i, j] = S[j, i] = similarity_metric(first_node_tags, second_node_tags)
            P[i, j] = P[j, i] = S[i, j] * A[i, j]
            total_P[i] += P[i, j]
            if i != j:
                total_P[j] += P[j, i]

    return total_P, P, S


def calculate_link_similarity(G, total_P, P, S, c, data_folder_name="similarity_propagation_data"):
    iteration = 0
    difference = 0

    while (iteration == 0 or difference > 0):
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
            np.save(data_folder_name + sep + "most_recent_S.npy", prev_S)
            sys.exit()
        iteration += 1


if __name__ == "__main__":
    G = read_graph()
    data_folder_name = "similarity_propagation_data"

    if not (path.exists(data_folder_name + sep + "results.txt")):
        total_P = P = S = None
        if not (path.exists(data_folder_name + sep + "total_P.npy") and path.exists(data_folder_name + sep + "P.npy") and (path.exists(data_folder_name + sep + "S.npy") or path.exists(data_folder_name + sep + "most_recent_S.npy"))):
            total_P, P, S = initialize_similarity_matrix(G)
            if not path.exists(data_folder_name):
                makedirs(data_folder_name)
            np.save(data_folder_name + sep + "total_P.npy", total_P)
            np.save(data_folder_name + sep + "P.npy", P)
            np.save(data_folder_name + sep + "S.npy", S)
        else:
            total_P = np.load(data_folder_name + sep + "total_P.npy")
            P = np.load(data_folder_name + sep + "P.npy")
            S = np.load(data_folder_name + sep + "most_recent_S.npy") if path.exists(data_folder_name +
                                                                                     sep + "most_recent_S.npy") else np.load(data_folder_name + sep + "S.npy")

        c = 1
        calculate_link_similarity(G, total_P, P, S, c)
        np.savetxt(data_folder_name + sep + "results.txt", S)
    else:
        S = np.loadtxt(data_folder_name + sep + "results.txt")
        print(test_correctness(G, S))
