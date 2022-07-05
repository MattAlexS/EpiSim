import networkx as nx
import numpy as np
import pandas as pd
import scipy.stats as ss
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('/Users/matthew/Desktop/CPPEpiSim/Graphs/303node31pack/')
FileList = glob.glob('*.grf')
in_file = pd.read_csv("303n31pSimStats.csv",header=None)

graphs = {}
pdist = {}

for graph in FileList:
    G = nx.read_adjlist(graph, nodetype=int)
    if G.number_of_nodes() == 303:
        graphs[graph] = G

for graph in graphs.keys():
    dists = []
    pathes = dict(nx.shortest_path_length(graphs[graph]))
    for i in range(303):
        for j in range(i+1,303):
            dists.append(pathes[i][j])
    pdist[graph] = np.asarray(dists)
            
stats = {}
performance = {}

for i in range(1,len(in_file),304):
    df = in_file.iloc[i+1:i+304,:]
    dft = df.T
    dft = dft.applymap(float)
    arr = dft.to_numpy()
    x = arr.mean(axis=0)
    #avgs.append(x)
    stats[in_file.iloc[i,0]] = x

for graph in graphs.keys():
    perf = stats[graph]
    diffs = []
    for i in range(len(perf)):
        for j in range(i+1, len(perf)):
            diffs.append(abs(perf[i]-perf[j]))
    performance[graph] = np.asarray(diffs)

corr = {}

for graph in graphs.keys():
    result = ss.linregress(pdist[graph],performance[graph])
    corr[graph] = result.rvalue

fig, axs = plt.subplots(5, 6)
fig.suptitle('Patient Zero Comparisson of Shortest Path Distance to Performance Difference')

for i in range(5):
    for j in range(6):
        graph = "Graph" + str(i*6 + j) + ".grf"
        x = pdist[graph]
        y = performance[graph]
        axs[i,j].scatter(x, y, alpha = 0.01)
        axs[i,j].set_title(graph)

for ax in axs.flat:
    ax.set(xlabel='Path Length', ylabel='RMSE Difference')


        
        




