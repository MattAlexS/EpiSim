import networkx as nx

for i in range(2,101):
    g = nx.random_regular_graph(1,100)
    print(nx.pagerank(g).values())
