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


def cosine_similarity(features1: set, features2: set):
    return len(features1.intersection(features2)) / (sqrt(len(features1)) * sqrt(len(features2))) if (sqrt(len(features1)) * sqrt(len(features2))) > 0 else 0


def jaccard_similarity(features1: set, features2: set):
    return len(features1.intersection(features2)) / len(features1.union(features2)) if len(features1.union(features2)) > 0 else 0

    
    

    
    



