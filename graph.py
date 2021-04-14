import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from constants import NUM_NODES


def create_graph():
    citations_file = open("./data/citations.dat")
    A = np.zeros(shape=(NUM_NODES, NUM_NODES), dtype=int)
    for i, line in enumerate(citations_file):
        split_line = line.split(" ")
        if len(split_line) > 1:
            for j in range(1, int(split_line[0]) + 1):
                A[i, int(split_line[j])] = 1
    citations_file.close()
    return nx.from_numpy_matrix(A)


def write_graph(G, filepath="./graph.txt"):
    nx.write_adjlist(G, filepath)


def read_graph(filepath="./graph.txt"):
    return nx.read_adjlist(filepath)
