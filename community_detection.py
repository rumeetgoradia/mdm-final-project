import csv
import os
import sys
from pathlib import Path

# pip install python-modularity-maximization==0.0.1rc4
from modularity_maximization import partition
from modularity_maximization.utils import get_modularity
from networkx.algorithms import community

from common import check_input_valid
from constants import DIRECTORY
from graph import read_graph


def get_communities(G):
    greedy_communities = community.greedy_modularity_communities
    print("GREEDY MODULARITY:", community.modularity(G, greedy_communities))
    print(len(list(greedy_communities)))
    # communities_generator = community.girvan_newman(G)
    # communities = next(communities_generator)
    # modularity = community.modularity(G, communities)

    # while (modularity < 0.5):
    #     print("MODULARITY:", str(modularity))
    #     prev_modularity = modularity
    #     prev_communities = communities
    #     communities = next(communities_generator)
    #     modularity = community.modularity(G, communities)
    #     if (modularity < prev_modularity):
    #         communities = prev_communities
    #         break

    # return np.array([list(c) for c in communities])

    communities = partition(G)
    for comm in set(communities.values()):
        print("Community %d" % comm)
    print("Modularity: %.3f" % get_modularity(G, communities))
    return communities


def write_communities(dataset: str, communities: dict):
    data_directory = os.path.join(DIRECTORY, "communities")
    Path(data_directory).mkdir(parents=True, exist_ok=True)
    # np.save(os.path.join(data_directory, dataset + "-communities.npy"), communities)
    with open(os.path.join(data_directory, dataset + "-communities.npy"), "w") as communities_file:
        writer = csv.writer(communities_file)
        for node, comm in communities.items():
            writer.writerow([node, comm])


def read_communities(dataset: str):
    communities = {}
    data_directory = os.path.join(DIRECTORY, "communities")
    with open(os.path.join(data_directory, dataset + "-communities.npy"), "r") as communities_file:
        reader = csv.reader(communities_file)
        for row in reader:
            communities[row[0]] = row[1]

    return communities


if __name__ == "__main__":
    dataset = check_input_valid(sys.argv)
    G = read_graph(dataset)

    communities = get_communities(G)
    write_communities(dataset, communities)
