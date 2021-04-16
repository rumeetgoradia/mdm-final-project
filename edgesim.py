import graph
import numpy as np
import networkx as nx
from constants import NUM_NODES

g = graph.create_graph() #could be done also from adj matrix

js_edges_np_matrix = np.zeroes(NUM_NODES)
l = range(0,NUM_NODES)
for i in l:
    ni = set(g[i])
    for j in l:
        if (i >= j):
            continue
        nj= set(g[j])
        js_edges_np_matrix[i,j] = len(ni.intersection(nj))/len(ni.union(nj))
        
