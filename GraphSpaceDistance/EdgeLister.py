import networkx as nx
import glob

graphs = {}
FileList = glob.glob('*.grf')

for file in FileList:
    graphs[file] = nx.read_edgelist(file)

for graph in graphs:
    nx.write_edgelist(graphs[graph], graph, data = False)
