import networkx as nx
import numpy as np


def create_graph():
    citations_file = open("./data/citations.dat")
    numNodes = len(citations_file.readlines())
    A = np.zeros(shape=(numNodes, numNodes), dtype=int)
    for i, line in enumerate(citations_file):
        split_line = line.split(" ")
        if len(split_line) > 1:
            for j in range(1, int(split_line[0])):
                A[i, j] = 1
    G = nx.from_numpy_matrix(A)
    return G


if __name__ == "__main__":
    create_graph()
