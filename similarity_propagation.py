import linecache

import networkx as nx
import numpy as np
from scipy.spatial.distance import cosine, jaccard
from tqdm import tqdm

from constants import NUM_NODES, NUM_TAGS
from graph import read_graph


def generate_tag_list(line: str):
    tags = np.zeros(shape=NUM_TAGS)
    split_line = line.split(" ")
    if len(split_line) > 1:
        for i in range(1, int(split_line[0]) + 1):
            tags[int(split_line[i])] = 1
    return tags


def cosine_similarity(v1, v2):
    return 1 - cosine(v1, v2)


def jaccard_similarity(v1, v2):
    return 1 - jaccard(v1, v2)


def initialize_similarity_matrix(G, similarity_metric=jaccard_similarity):
    A = nx.adjacency_matrix(G)
    total_P = dict.fromkeys(G.nodes, 0.0)
    P = np.zeros(shape=A.shape)
    S = np.zeros(shape=A.shape)
    tags_file = open('./data/item-tag.dat')
    for i, line in tqdm(enumerate(tags_file)):
        first_node_tags = generate_tag_list(line)
        for j in range(i, NUM_NODES):
            second_node_tags = generate_tag_list(linecache.getline('./data/item-tag.dat', j))
            S[i, j] = S[j, i] = similarity_metric(first_node_tags, second_node_tags)
            P[i, j] = P[j, i] = S[i, j] * A[i, j]
            total_P[i] += P[i, j]
            if i != j:
                total_P[j] += P[j, i]

    tags_file.close()
    return total_P, P, S


if __name__ == '__main__':

    # G = read_graph()
    # total_P, P, S = initialize_similarity_matrix(G)
    # print(total_P)
    # print(P)
    # print(S)
    tags = generate_tag_list(linecache.getline('./data/item-tag.dat', 1))
    print(tags.shape)
    print(np.sum(tags))
