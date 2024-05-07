import networkx as nx
import random
import numpy as np
from scipy.stats import skew
import os
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

def dist(graph1, graph2):
    out = np.linalg.norm(graph1-graph2)
    return out

legend = ["DCvPR","DCvDgSq", "DCvM", "DCvSD", "DCvSK", "DCvMSD",
          "PRvDgSq", "PRvM", "PRvSD", "PRvSK", "PRvMSD",
          "DgSqvM", "DgSqvSD", "DgSqvSK", "DgSqvMSD",
          "MvSD", "MvSK", "MvMSD",
          "SDvSK", "SDvMSD",
          "SKvMSD"]

corrs = {}
correlate = []
sizes = []
sample_num = 50
for i in range(5,406,20):
    sizes.append(i)
    dists = [[],[],[],[],[],[],[]]
    dcs = []
    prs = []
    degseqs = []
    means = []
    sds = []
    skews = []
    meansds = []
    graph_name = str(i) + "PLC0.grf"
    dc_name = str(i) + "PLC0.dc"
    os.chdir("/Users/matthew/Desktop/COVID Vaccination Project/Point Packing Graphs/GraphSizeCorrelationExperiment/PLCgraphs/")
    g = nx.read_adjlist(graph_name)
    os.chdir("/Users/matthew/Desktop/COVID Vaccination Project/Point Packing Graphs/GraphSizeCorrelationExperiment/PLCdcs/")
    dc = np.empty(i,dtype = float)
    with open(dc_name, 'r') as file:
        data = file.readlines()
        strdc = data[0].strip().split(',')
    for x in range(len(strdc)):
        dc[x] = float(strdc[x])
    dcs.append(dc)
    prs.append(np.asarray(list(nx.pagerank(g).values())))
    degseq = np.asarray(sorted([d for n, d in g.degree()]))
    degseqs.append(degseq)
    means.append(np.mean(degseq))
    sds.append(np.std(degseq))
    skews.append(skew(degseq))
    meansds.append(np.array([np.mean(degseq),np.std(degseq)]))
    for samp in range(1,sample_num):
        graph_name = str(i) + "PLC" + str(samp) + ".grf"
        dc_name = str(i) + "PLC" + str(samp) + ".dc"
        os.chdir("/Users/matthew/Desktop/COVID Vaccination Project/Point Packing Graphs/GraphSizeCorrelationExperiment/PLCgraphs/")
        g = nx.read_adjlist(graph_name)
        os.chdir("/Users/matthew/Desktop/COVID Vaccination Project/Point Packing Graphs/GraphSizeCorrelationExperiment/PLCdcs/")
        dc = np.empty(i,dtype = float)
        with open(dc_name, 'r') as file:
            data = file.readlines()
            strdc = data[0].strip().split(',')
        for x in range(len(strdc)):
            dc[x] = float(strdc[x])
        pr = np.asarray(list(nx.pagerank(g).values()))
        degseq = np.asarray(sorted([d for n, d in g.degree()]))
        mean = np.mean(degseq)
        sd = np.std(degseq)
        sk = skew(degseq)
        meansd = np.array([mean,sd])
        for z in range(len(dcs)):
            dists[0].append(dist(dc,dcs[z]))
            dists[1].append(dist(pr,prs[z]))
            dists[2].append(dist(degseq,degseqs[z]))
            dists[3].append(abs(mean-means[z]))
            dists[4].append(abs(sd-sds[z]))
            dists[5].append(abs(sk-skews[z]))
            dists[6].append(dist(meansd,meansds[z]))
        dcs.append(dc)
        prs.append(pr)
        degseqs.append(degseq)
        means.append(mean)
        sds.append(sd)
        skews.append(sk)
        meansds.append(meansd)
    np.asarray(dists)
    r = np.corrcoef(dists)
    corrs[i] = [str(r[0,1]), str(r[0,2]), str(r[0,3]), str(r[0,4]), str(r[0,5]), str(r[0,6]),
                str(r[1,2]), str(r[1,3]), str(r[1,4]), str(r[1,5]), str(r[1,6]),
                str(r[2,3]), str(r[2,4]), str(r[2,5]), str(r[2,6]),
                str(r[3,4]), str(r[3,5]), str(r[3,6]),
                str(r[4,5]), str(r[4,6]),
                str(r[5,6])]
    correlate.append([r[0,1], r[0,2], r[0,3], r[0,4], r[0,5], r[0,6],
                r[1,2], r[1,3], r[1,4], r[1,5], r[1,6],
                r[2,3], r[2,4], r[2,5], r[2,6],
                r[3,4], r[3,5], r[3,6],
                r[4,5], r[4,6],
                r[5,6]])

y = np.asarray(correlate)
x = np.asarray(sizes).reshape((-1, 1))

for z in range(21):
    Y = y[:,z]
    X = x
    X = sm.add_constant(X)
    results = sm.GLS(Y,X).fit()
    conf = results.conf_int()
    #if conf[1,0] <= 0 and conf[1,1] >= 0:
    #    print("Slope = 0")
    #else:
    print(str(round(conf[1,0],5)) + "***Slope***" + str(round(conf[1,1],5))) #add indent on this line if removing
    print(str(round(conf[0,0],5)) + "***" + legend[z] + "***" + str(round(conf[0,1],5)))
    print(str(results.rsquared))



"""
os.chdir("/Users/matthew/Desktop/COVID Vaccination Project/Point Packing Graphs/GraphSizeCorrelationExperiment/")
with open("correlation.csv", "w") as file:
    print("#ofNodes," + ",".join(legend), file = file)
    for i in corrs:
        print(str(i) + "," + ",".join(corrs[i]), file = file)
"""
