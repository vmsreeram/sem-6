import networkx as nx
import matplotlib.pyplot as plt
import random
import tqdm

class Lattice:
    def __init__(self, n):
        self.G = nx.empty_graph()
        for i in range(n):
            for j in range(n):
                self.G.add_node((i,j))
        self.n = n
        # self.__path=[-1,-1]
        
    def show(self):
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        nx.draw(self.G,node_shape='o', node_size=0.05, node_color='blue', pos=pos, with_labels=False,edge_color='r')       
        plt.show()
        # plt.savefig('.Q5_show.png')
        
    def percolate(self, p):
        for node in self.G.nodes():
            if node[0]<self.n-1:
                self.G.add_edge(node,(node[0]+1,node[1]))
            if node[1]<self.n-1:
                self.G.add_edge(node,(node[0],node[1]+1))
            if node[0]>0:
                self.G.add_edge(node,(node[0]-1,node[1]))
            if node[1]>0:
                self.G.add_edge(node,(node[0],node[1]-1))
        
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
                    # self.__path=[u,v]
                    return True
        return False
    
    def showPaths(self):
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        top_nodes = [(0, i) for i in range(self.n)]
        bottom_nodes = [(self.n - 1, i) for i in range(self.n)]
        nx.draw(self.G,node_shape='o', node_size=0.05, node_color='blue', pos=pos, with_labels=False,edge_color='r')
        for u in tqdm.tqdm(top_nodes):
            # print("u =",u)
            shortest_path_to_bottom = None
            for v in bottom_nodes:
                if nx.has_path(self.G, u, v):
                    thispath = nx.shortest_path(self.G, u, v)
                    if(shortest_path_to_bottom==None or len(thispath)<len(shortest_path_to_bottom)):
                        shortest_path_to_bottom=thispath
            
            if shortest_path_to_bottom != None:
                path_edges = list(zip(shortest_path_to_bottom,shortest_path_to_bottom[1:]))
                nx.draw_networkx_edges(self.G,node_size=0.5,pos=pos,edgelist=path_edges,edge_color = 'green', width=2)
                continue
            
            lengths = nx.single_source_dijkstra_path_length(self.G, u)  # Get the length of the longest path from node to any other node
            dest = max(lengths, key=lengths.get)                        # Get the node with the longest path
            path = nx.dijkstra_path(self.G, u, dest)                    # Get the actual longest path
            # print("path =",path)
            path_edges = list(zip(path,path[1:]))                       # Get the edge lists
            # print("path_edges =",path_edges)
            nx.draw_networkx_edges(self.G,node_size=0.5,pos=pos,edgelist=path_edges,edge_color = 'green', width=2)
            
        plt.savefig('.Q5_showpaths.png')
        plt.show()

    
l = Lattice(100)
l.show()
l.percolate(0.5)
l.show()
print(l.existsTopDownPath())

l.showPaths()