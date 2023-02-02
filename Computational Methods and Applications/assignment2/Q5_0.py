import networkx as nx
import matplotlib.pyplot as plt
import random

class Lattice:
    def __init__(self, n):
        self.G = nx.grid_2d_graph(n, n)

    def show(self):
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        nx.draw(self.G, node_size=5, pos=pos, with_labels=False,edge_color='r')        
        plt.show()

    def percolate(self, p):
        for edge in self.G.edges():
            if random.uniform(0, 1) < p:
                self.G[edge[0]][edge[1]]['weight'] = 1
            else:
                self.G[edge[0]][edge[1]]['weight'] = 0
                self.G.remove_edge(edge[0], edge[1])

    def existsTopDownPath(self):
        top_nodes = [(0, i) for i in range(self.G.shape[0])]
        bottom_nodes = [(self.G.shape[0]-1, i) for i in range(self.G.shape[0])]
        for node in top_nodes:
            if nx.has_path(self.G, node, bottom_nodes[0]):
                return True
        return False

    def showPaths(self):
        top_nodes = [(0, i) for i in range(self.G.shape[0])]
        bottom_nodes = [(self.G.shape[0]-1, i) for i in range(self.G.shape[0])]
        paths = []
        for node in top_nodes:
            path_exists = False
            for bottom_node in bottom_nodes:
                if nx.has_path(self.G, node, bottom_node):
                    paths.append(nx.shortest_path(self.G, node, bottom_node))
                    path_exists = True
                    break
            if not path_exists:
                paths.append(nx.dijkstra_path(self.G, node, bottom_nodes[0]))
        nx.draw(self.G, node_size=50, with_labels=False)
        nx.draw_networkx_edges(self.G, pos=nx.spring_layout(self.G), edgelist=paths, edge_color='r', width=2)
        plt.show()

l = Lattice(25)
l.percolate(0.4)
print(l.existsTopDownPath())

l.show()