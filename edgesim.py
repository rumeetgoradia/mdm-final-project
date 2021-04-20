import graph
import numpy as np
import networkx as nx
from constants import NUM_NODES
import linecache

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

def tagsim(g): 
    # loop through g
    # same as above, but grab tag values from item-tag.dat
    # set intersection etc
    tagsim_edges_matrix = np.zeros((NUM_NODES,NUM_NODES))
    l = range(0,NUM_NODES)
    for i in l:
        if(len(g[i]) != 0):
            linegi = linecache.getline("./data/item-tag.dat",i)
            spl = linegi.split(" ")
            if int(spl[0]) > 0:
                tagset1 = set()
                for j in range(1,len(spl)):
                    tagset1.add(spl[j])
                for element in g[i]:
                    line_e = linecache.getline("./data/item-tag.dat",element)
                    spl = line_e.split(" ")
                    tagset2 = set()
                    if (int(spl[0]) > 0):
                        for k in range(1,len(spl)):
                            tagset2.add(spl[k])
                        tagsim_edges_matrix[i,element] = len(tagset2.intersection(tagset1))/len(tagset2.union(tagset1))
    return tagsim_edges_matrix

def commonneighbors(g):
    cn_edges_np_matrix = np.zeros((NUM_NODES,NUM_NODES))
    l = range(0,NUM_NODES)
    for i in l:
        print(str(i) + " of " + str(NUM_NODES))
        ni = set(g[i])
        if(len(ni) != 0):
            for j in l:
                if (i >= j):
                    continue
                nj= set(g[j])
                cn_edges_np_matrix[i,j] = len(ni.intersection(nj))
    return cn_edges_np_matrix

g = graph.create_graph() #could be done also from adj matrix
sol = edgesimilarity(g)
np.save('similarities/edgesim',sol)

#might make sense to just change the weight of each edge to the jc. sim, then return the graph