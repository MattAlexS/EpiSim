import pandas as pd
import networkx as nx
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

#os.chdir("/Users/matthew/Desktop/CPPEpiSim/")

FileList = glob.glob('*.grf')

def dist(graph1, graph2):
    out = np.linalg.norm(graph1-graph2)
    return out

degree = []
pr = []
mean = []
sd = []
skew = []
minmin = []
nodeavg = []
graphavg = []

ddist = []
prdist = []
meandiff = []
sdiff = []
meansdist = []
skewdiff = []
mindiff = []
nodediff = []
avgdiff = []



for graph in FileList:
    G = nx.read_adjlist(graph, nodetype=int)
    if G.number_of_nodes() == 303:
        dseq = np.asarray(sorted([d for n, d in G.degree()]))
        degree.append(dseq)
        mean.append(dseq.mean())
        sd.append(dseq.std())
        skew.append(ss.skew(dseq))
        pr.append(np.asarray(sorted(nx.pagerank(G).values())))


in_file = pd.read_csv("303n31pSimStats.csv",header=None)
for i in range(1,len(in_file),304):
    df = in_file.iloc[i+1:i+304,:]
    means = np.asarray(df.mean(axis = 1))
    minnode = np.argmin(means)
    nodeavg.append(means[minnode])
    graphavg.append(means.mean())
    minmin.append(df.min().min())

for i in range(len(degree)-1):
    for j in range(i+1,len(degree)):
        ddist.append(dist(degree[i],degree[j]))
        prdist.append(dist(pr[i],pr[j]))
        meandiff.append(abs(mean[i] - mean[j]))
        sdiff.append(abs(sd[i] - sd[j]))
        skewdiff.append(abs(skew[i] - skew[j]))
        meansdist.append(dist(np.asarray([mean[i],sd[i]]),np.asarray([mean[j],sd[j]])))
        mindiff.append(abs(minmin[i] - minmin[j]))
        nodediff.append(abs(nodeavg[i] - nodeavg[j]))
        avgdiff.append(abs(graphavg[i] - graphavg[j]))

df = pd.DataFrame()
df['Degree Sequence'] = ddist
df['PageRank'] = prdist
df['Mean'] = meandiff
df['Standard Deviation'] = sdiff
df['Skew'] = skewdiff
df['Mean SD'] = meansdist
df['Min RMSE'] = mindiff
df['Min Node RMSE'] = nodediff
df['Avg RMSE'] = avgdiff

corrMatrix = df.corr()
sns.heatmap(corrMatrix, annot=True)
plt.show()
        
        







    

