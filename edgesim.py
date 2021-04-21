import graph
import numpy as np
import networkx as nx
from constants import NUM_NODES
import linecache
from common import test_correctness

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
                js_edges_np_matrix[j,i] = js_edges_np_matrix[i,j]
    return js_edges_np_matrix

def tagsim(g): 
    # loop through g
    # same as above, but grab tag values from item-tag.dat
    # set intersection etc
    tagsim_edges_matrix = np.zeros((NUM_NODES,NUM_NODES))
    l = range(0,NUM_NODES)
    for i in l:
        print(str(i) + " of " + str(NUM_NODES))
        if(len(g[i]) != 0):
            linegi = linecache.getline("./data/item-tag.dat",i+1)
            spl = linegi.split(' ')
            if int(spl[0]) > 0:
                tagset1 = set()
                for j in range(1,len(spl)):
                    tagset1.add(spl[j])
                for element in g[i]:
                    line_e = linecache.getline("./data/item-tag.dat",element+1)
                    spl = line_e.split(" ")
                    tagset2 = set()
                    if (int(spl[0]) > 0):
                        for k in range(1,len(spl)):
                            tagset2.add(spl[k])
                        tagsim_edges_matrix[i,element] = len(tagset2.intersection(tagset1))/len(tagset2.union(tagset1))
                        tagsim_edges_matrix[i,element] = tagsim_edges_matrix[element,i]
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
                cn_edges_np_matrix[j,i] = cn_edges_np_matrix[i,j] 
    return cn_edges_np_matrix

g = graph.create_graph() #could be done also from adj matrix

print("Edge Sim")
es = test_correctness(g,edgesimilarity(g))

print("Tag Sim")
ts = test_correctness(g,tagsim(g))

print("Common Neighbors")
cn = test_correctness(g,commonneighbors(g))
print("Edge Similarity using Jaccard Sim: " + str(es))
print("Tag Sim using Jaccard Sim: " + str(ts))
print("Common Neighbors " + str(cn))

#might make sense to just change the weight of each edge to the jc. sim, then return the graph
