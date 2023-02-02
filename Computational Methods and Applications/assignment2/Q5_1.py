import networkx as nx
import matplotlib.pyplot as plt
import random

class Lattice:
    
    def __init__(self, n):
        self.G = nx.grid_2d_graph(n, n)
        self.n = n
        
    def show(self):
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        nx.draw(self.G, node_size=1, pos=pos, with_labels=False,edge_color='r')        
        plt.show()
        
    def percolate(self, p):
        for edge in self.G.edges():
            if random.uniform(0, 1) < p:
                self.G[edge[0]][edge[1]]['weight'] = 1
            else:
                self.G[edge[0]][edge[1]]['weight'] = 0
                self.G.remove_edge(edge[0], edge[1])
                
    def existsTopDownPath(self):
        top_nodes = [(0, i) for i in range(self.n)]
        bottom_nodes = [(self.n - 1, i) for i in range(self.n)]
        for u in top_nodes:
            for v in bottom_nodes:
                if nx.has_path(self.G, u, v):
                    return True
        return False
    
    def showPaths(self):
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        top_nodes = [(0, i) for i in range(self.n)]
        bottom_nodes = [(self.n - 1, i) for i in range(self.n)]
        for u in top_nodes:
            for v in bottom_nodes:
                if nx.has_path(self.G, u, v):
                    path = nx.shortest_path(self.G, u, v)
                    nx.draw_networkx_nodes(self.G,node_size=1, pos=pos, nodelist=path, node_color='b')
                else:
                    largest_shortest_path = max(nx.shortest_path_length(self.G, u).values())
                    nodes = [v for v in self.G.nodes() if nx.shortest_path_length(self.G, u)[v] == largest_shortest_path]
                    nx.draw_networkx_nodes(self.G,node_size=1, pos=pos, nodelist=nodes, node_color='b')
        plt.show()

l = Lattice(10)
l.percolate(0.4)
# l.show()
print(l.existsTopDownPath())

l.showPaths()