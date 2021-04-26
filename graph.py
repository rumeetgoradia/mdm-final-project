import csv
import json
import os

import networkx as nx
import numpy as np
from tqdm import tqdm

from constants import DATASETS, DIRECTORY, NUM_NODES


def create_graph(dataset: str):
    A = np.zeros(shape=(NUM_NODES[dataset], NUM_NODES[dataset]), dtype=int)
    if dataset == "citeulike":
        with open(os.path.join(DIRECTORY, "data", dataset, "edges.dat"), "r") as edges_file:
            for i, line in enumerate(edges_file):
                split_line = line.split(" ")
                if len(split_line) > 1:
                    for j in range(1, int(split_line[0]) + 1):
                        A[i, int(split_line[j])] = 1
    else:
        with open(os.path.join(DIRECTORY, "data", dataset, "edges.csv"), "r") as edges_file:
            reader = csv.reader(edges_file)
            next(reader)
            for row in reader:
                A[int(row[0]), int(row[1])] = 1
                A[int(row[1]), int(row[0])] = 1

    return nx.from_numpy_matrix(A)


def write_graph(G, dataset: str):
    nx.write_adjlist(G, os.path.join(DIRECTORY, "graphs", dataset + "-graph.txt"))


def read_graph(dataset: str):
    G = None
    try:
        G = nx.read_adjlist(os.path.join(DIRECTORY, "graphs", dataset + "-graph.txt"), nodetype=int)
    except:
        G = create_graph(dataset)
        write_graph(G, dataset)

    return G


def extract_features(dataset: str):
    features = {}
    if (dataset == "citeulike"):
        with open(os.path.join(DIRECTORY, "data", dataset, "features.dat"), "r") as features_file:
            for i, line in enumerate(features_file):
                split_line = line.split(" ")
                features_set = set()
                if len(split_line) > 1:
                    for j in range(1, int(split_line[0]) + 1):
                        features_set.add(int(split_line[j]))
                features[i] = features_set
    else:
        with open(os.path.join(DIRECTORY, "data", dataset, "features.json"), "r") as features_file:
            features_data = json.load(features_file)
            for i in range(NUM_NODES[dataset]):
                if str(i) in features_data:
                    features[i] = set(features_data[str(i)])
                else:
                    features[i] = set()

    return features


if __name__ == "__main__":
    for dataset in DATASETS:
        print("Creating graph for", dataset, "dataset")        
        G = create_graph(dataset)
        write_graph(G, dataset)
