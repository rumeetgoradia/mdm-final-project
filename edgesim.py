import graph
import numpy as np
import networkx as nx
from constants import NUM_NODES

def edgesimilarity(g):
    js_edges_np_matrix = np.zeros((NUM_NODES,NUM_NODES))
    l = range(0,NUM_NODES)
    for i in l:
        print(str(i) + " of " + str(NUM_NODES))
        ni = set(g[i])
        if(len(ni) != 0):
            for j in l:
                if (i >= j):
                    continue
                nj= set(g[j])
                js_edges_np_matrix[i,j] = len(ni.intersection(nj))/len(ni.union(nj))
    return js_edges_np_matrix
        

g = graph.create_graph() #could be done also from adj matrix
sol = edgesimilarity(g)

np.savetxt('t.txt',sol,delimiter=',',fmt='%.2e')

#might make sense to just change the weight of each edge to the jc. sim, then return the graph