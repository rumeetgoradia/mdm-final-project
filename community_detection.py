import csv
import os
from pathlib import Path

from networkx.algorithms import community
from tqdm import tqdm

from constants import DATASETS, DIRECTORY
from graph import read_graph


def generate_communities(G):
    communities_list = list(community.greedy_modularity_communities(G))
    print("# of Communities:", str(len(communities_list)))
    print("Modularity:", str(community.modularity(G, communities_list)))

    communities = {}
    for i, comm in enumerate(communities_list):
        for node in comm:
            communities[node] = i
    return communities


def write_communities(dataset: str, communities: dict):
    data_directory = os.path.join(DIRECTORY, "communities")
    Path(data_directory).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(data_directory, dataset + "-communities.csv"), "w") as communities_file:
        writer = csv.writer(communities_file)
        for node, comm in communities.items():
            writer.writerow([node, comm])


def read_communities(dataset: str):
    communities = {}
    data_directory = os.path.join(DIRECTORY, "communities")

    try:
        with open(os.path.join(data_directory, dataset + "-communities.csv"), "r") as communities_file:
            reader = csv.reader(communities_file)
            for row in reader:
                communities[int(row[0])] = int(row[1])
    except:
        G = read_graph(dataset)
        communities = generate_communities(G)
        write_communities(dataset, communities)

    return communities


if __name__ == "__main__":
    for dataset in DATASETS:
        print("Detecting communities for", dataset, "dataset")        
        G = read_graph(dataset)
        communities = generate_communities(G)
        write_communities(dataset, communities)
