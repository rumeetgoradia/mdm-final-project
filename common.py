import random
import sys
from math import sqrt

import networkx as nx
import numpy as np
from tqdm import tqdm

from constants import DATASETS


def check_input_valid(args: list):
    if (len(args) < 2 or args[1] not in DATASETS):
        print("Please choose a dataset from the following list to run this file.")
        print(DATASETS)
        sys.exit()
    else:
        return args[1]


def cosine_similarity(set1: set, set2: set):
    return len(set1.intersection(set2)) / (sqrt(len(set1)) * sqrt(len(set2))) if (sqrt(len(set1)) * sqrt(len(set2))) > 0 else 0


def jaccard_similarity(set1: set, set2: set):
    return len(set1.intersection(set2)) / len(set1.union(set2)) if len(set1.union(set2)) > 0 else 0


def test_correctness(G, S, n=50000):
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

    # print("SUCCESS:", str(success_count))
    # print("TIE:", str(tie_count))
    return (success_count + 0.5 * tie_count) / n


def precision_testing(G, S, ds, thresh=0.75, sample_size=30, edges_removed=100):
    trials = 0
    test = 0
    while test < sample_size:
        removed_edges = {}
        i = 0
        while(i < edges_removed):  # random removal of edges
            rnd_node_1 = random.randint(0, DATASETS[ds]-1)
            node_1_index = random.randint(0, len(list(G.edges(rnd_node_1))))
            G.remove_edge(rnd_node_1, node_1_index)
            if not ((nx.number_connected_components(G) == 1) and (len(G.nodes) == DATASETS[ds])):
                G.add_edge(rnd_node_1, node_1_index)
                continue
            if rnd_node_1 in removed_edges.keys():
                removed_edges[rnd_node_1].append(node_1_index)
            else:
                removed_edges[rnd_node_1] = []
                removed_edges[rnd_node_1].append(node_1_index)
            i = i + 1
        i = j = 0
        total_positive = 0
        true_positive = 0
        while i < DATASETS[ds]-1:
            while j < DATASETS[ds]-1:
                if S[i][j] >= thresh:
                    if(not G.has_edge(i, j)):
                        if(i in removed_edges.keys()):  # double counting true/all positives
                            if(j in removed_edges[i]):
                                true_positive = true_positive + 1
                                total_positive = total_positive + 1
                            else:
                                total_positive = total_positive + 1
                        elif(j in removed_edges.keys()):
                            if(i in removed_edges[j]):
                                true_positive = true_positive + 1
                                total_positive = total_positive + 1
                            else:
                                total_positive = total_positive + 1
                        else:
                            total_positive = total_positive + 1
                j = j + 1
            i = i + 1
        for n1, v in removed_edges:
            for n2 in v:
                G.add_edge(n1, n2)
        trials = trials + ((true_positive)/total_positive)*0.5
        test = test + 1
    return trials/sample_size
