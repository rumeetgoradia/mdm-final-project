import graph
import numpy as np
import networkx as nx
from constants import NUM_NODES
import linecache
import testing
from tqdm import tqdm
from constants import DATASETS

def edgesimilarity(g,ds):
    js_edges_np_matrix = np.zeros((NUM_NODES[ds],NUM_NODES[ds]))
    l = range(0,NUM_NODES[ds])
    for i in tqdm(l,desc = "Jac. Edge Sim Calculation"):
        ni = set(g[i])
        if(len(ni) != 0):
            for j in l:
                if (i >= j):
                    continue
                nj= set(g[j])
                js_edges_np_matrix[i,j] = len(ni.intersection(nj))/len(ni.union(nj))
                js_edges_np_matrix[j,i] = js_edges_np_matrix[i,j]
    return js_edges_np_matrix

def tagsim(g,ds): 
    # loop through g
    # same as above, but grab tag values from item-tag.dat
    # set intersection etc
    tagsim_edges_matrix = np.zeros((NUM_NODES[ds],NUM_NODES[ds]))
    l = range(0,NUM_NODES[ds])
    for i in l:
        print(str(i) + " of " + str(NUM_NODES[ds]))
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

def commonneighbors(g,ds):
    cn_edges_np_matrix = np.zeros((NUM_NODES[ds],NUM_NODES[ds]))
    l = range(0,NUM_NODES[ds])
    for i in l:
        ni = set(g[i])
        if(len(ni) != 0):
            for j in l:
                if (i >= j):
                    continue
                nj= set(g[j])
                cn_edges_np_matrix[i,j] = len(ni.intersection(nj))
                cn_edges_np_matrix[j,i] = cn_edges_np_matrix[i,j] 
    return cn_edges_np_matrix


'''
dataset = "twitch-ru"
G = graph.read_graph(dataset)
s = 0
for i in (range(30)):
    G, removed_edges = testing.edge_removal(G,dataset,edges_removed = 500)
    print("Finished Removing Edges")
    s = s + testing.precision_testing(G,removed_edges,edgesimilarity(G,dataset),dataset)
    print("Finished Precision Testing")
    testing.edge_addback(G,removed_edges)
    print("Added Back Edges")
print(s/30)
'''
#might make sense to just change the weight of each edge to the jc. sim, then return the graph
