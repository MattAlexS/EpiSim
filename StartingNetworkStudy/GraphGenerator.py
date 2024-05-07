import networkx as nx
import random
import os
os.chdir("/Users/matthew/Desktop/COVID Vaccination Project/Point Packing Graphs/GraphSizeCorrelationExperiment/PLCgraphs/")


sample_num = 50
for i in range(5,725,20):
    for samp in range(sample_num):
        filename = str(i) + "PLC" + str(samp) + ".grf"
        m = random.randint(1,i-1)
        p = random.random()
        g = nx.powerlaw_cluster_graph(i,m,p)
        nx.write_adjlist(g,filename)

