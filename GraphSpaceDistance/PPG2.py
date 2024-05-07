import networkx as nx
import numpy as np
import random
import statistics
import os

def evaluate(individual):
    a = len(individual)
    return a

def dist(graph1, graph2):
    out = np.linalg.norm(graph1-graph2)
    return out

def generate(nodes, max_edges, size):
    points = []
    for i in range(size):
        connected = False
        while connected == False:
            edge_num = random.randint(1,max_edges)
            p = random.random()
            new = nx.powerlaw_cluster_graph(nodes, edge_num, p)
            connected = nx.is_connected(new)
        #pr = np.asarray(sorted(nx.pagerank(new).values()))
        degree_seq = np.asarray([d for n, d in new.degree()])
        coords = np.asarray([np.mean(degree_seq),np.std(degree_seq)])
        points.append([new, coords])
    return points

def reduce(points, dist_thresh):
    packing = []
    packing.append(points[0])
    for i in range(len(points)):
        count = 0
        for graph in packing:
            if dist(graph[1],points[i][1]) >= dist_thresh:
                count += 1
        if count == len(packing):
            packing.append(points[i])
    return packing
    
def initialize(nodes, max_edges, size, dist_thresh):
    out = reduce(generate(nodes, max_edges, size), dist_thresh)
    return out

def mate(mom, dad, nodes, max_edges, rmr, dist_thresh):
    new = []
    new.extend(mom)
    new.extend(dad)
    mutation = generate(nodes, max_edges, rmr)
    new.extend(mutation)
    random.shuffle(new)
    out = reduce(new, dist_thresh)
    return out

POP_SIZE = 100
INIT_IND_SIZE = 5
MIN_DIST = 2.25#0.015
MAX_EDGES = 60
NODE_NUM = 160
GEN_NUM = 100
MATINGS = 200
RMR = 2
TOURN_SIZE = 3

avg = []
low = []
high = []
pop = []
for i in range(POP_SIZE):
    pop.append(initialize(NODE_NUM, MAX_EDGES, INIT_IND_SIZE, MIN_DIST))

for i in range(GEN_NUM):
    print(i)
    new = []
    children = []
    fitnesses = []
    for j in range(MATINGS):
        parents = random.choices(pop, k = 2)
        child = mate(parents[0], parents[1], NODE_NUM, MAX_EDGES, RMR, MIN_DIST)
        children.append(child)
    pop.extend(children)
    for j in range(POP_SIZE):
        tournament = random.choices(pop, k = TOURN_SIZE)
        winner = max(tournament, key=evaluate)
        new.append(winner)
        fitnesses.append(evaluate(winner))
    avg.append(statistics.mean(fitnesses))
    low.append(min(fitnesses))
    high.append(max(fitnesses))
    pop = new

"""
script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, 'Packings/303n32pMeanSD/')

for ind in pop:
    if len(ind) == high[-1]:
        break

for i in range(len(ind)):
    fh = open(results_dir + "Graph" + str(i) + ".grf", "wb")
    nx.write_adjlist(ind[i][0], fh)
    
        
"""     
        
    





    

