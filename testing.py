import random
import sys
from math import sqrt
import networkx as nx
import numpy as np
from tqdm import tqdm

from constants import DATASETS

def edge_removal(G,ds,edges_removed = 100):
    removed_edges = {}
    i = 0
    while(i < edges_removed): #random removal of edges
        rnd_node_1 = random.randint(0,DATASETS[ds]-1)
        node_1_index = random.randint(0,len(list(G.edges(rnd_node_1))))
        G.remove_edge(rnd_node_1,node_1_index)
        if not ((nx.number_connected_components(G) == 1) and (len(G.nodes) == DATASETS[ds])): #ensure no single edges btw two nodes are cut, graph is conn
            G.add_edge(rnd_node_1,node_1_index)
            continue
        if rnd_node_1 in removed_edges.keys():
            removed_edges[rnd_node_1].append(node_1_index)
        else:
            removed_edges[rnd_node_1] = []
            removed_edges[rnd_node_1].append(node_1_index)
        i = i + 1
    return G, removed_edges

def edge_addback(G,removed_edges): #young laflame sicko mode
    for n1, v in removed_edges:
        for n2 in v:
            G.add_edge(n1,n2)
    return G

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
def precision_testing(G,removed_edges,S,ds,thresh = 0.75): 
    # before using this function, you must randomly remove edges using the
    # edge removal method, and then pass in the result
    # after the method has ended, add back in the edges you have removed
    # using the edges addback method
    i = j = 0
    total_positive = 0
    true_positive = 0
    while i < DATASETS[ds]-1: 
        while j < DATASETS[ds]-1:
            if S[i][j] >= thresh:
                if(not G.has_edge(i,j)):
                    if(i in removed_edges.keys()): #double counting true/all positives
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
    return ((true_positive)/total_positive)*0.5
