import networkx as nx
import matplotlib.pyplot as plt
import random
import tqdm

class Lattice:
    def __init__(self, n):
        if type(n)!=int or n<0:                             # disallow illegal values of n
            raise ValueError("Inappropriate argument: expected non negative int")
        
        self.G = nx.empty_graph()                           # construct an empty nx graph and add nodes to it
        for i in range(n):
            for j in range(n):
                self.G.add_node((i,j))
        self.n = n
        # self.__path=[-1,-1]
        
    def show(self):                                         # display the image of the lattice
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}      # to fix position of nodes of the lattice as in x-y coordinate system. (y,-x) is used so that it matches with the convension used below in showPaths()
        nx.draw(self.G,node_shape='o', node_size=0.05, node_color='blue', pos=pos, with_labels=False,edge_color='r')       
        plt.show()
        # plt.savefig('.Q5_show.png')
        
    def percolate(self, p):
        # adds all possible legal edges first
        for node in self.G.nodes():
            if node[0]<self.n-1:
                self.G.add_edge(node,(node[0]+1,node[1]))
            if node[1]<self.n-1:
                self.G.add_edge(node,(node[0],node[1]+1))
            if node[0]>0:
                self.G.add_edge(node,(node[0]-1,node[1]))
            if node[1]>0:
                self.G.add_edge(node,(node[0],node[1]-1))
        
        # then removes edges based on sampling outcome
        for edge in self.G.edges():
            if random.uniform(0, 1) > p:
                self.G.remove_edge(edge[0], edge[1])
                
    def existsTopDownPath(self):                            # returns True if there exist some path from some top level node to any bottom level node.
        top_nodes = [(0, i) for i in range(self.n)]         # convention I used here is (depth from x-axis,shift from y-axis)
        bottom_nodes = [(self.n - 1, i) for i in range(self.n)]
        for u in top_nodes:
            for v in bottom_nodes:
                if nx.has_path(self.G, u, v):               # returns True if a path exists from u to v in self.G
                    # self.__path=[u,v]
                    return True
        return False                                        # return False if no path exist from any top vertex to any bottom vertex
    
    def showPaths(self):
        pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        top_nodes = [(0, i) for i in range(self.n)]         # convention I used here is (depth from x-axis,shift from y-axis)
        bottom_nodes = [(self.n - 1, i) for i in range(self.n)]
        
        # drawing the pre-path computing version of the lattice, so that we can later overlay the computed path.
        nx.draw(self.G,node_shape='o', node_size=0.05, node_color='blue', pos=pos, with_labels=False,edge_color='r')
        
        for u in tqdm.tqdm(top_nodes):
            # print("u =",u)
            # computing the shortest path from u to any bottom level vertex.
            shortest_path_to_bottom = None
            for v in bottom_nodes:
                if nx.has_path(self.G, u, v):
                    thispath = nx.shortest_path(self.G, u, v)
                    if(shortest_path_to_bottom==None or len(thispath)<len(shortest_path_to_bottom)):
                        shortest_path_to_bottom=thispath
            
            if shortest_path_to_bottom != None:
                # since we got a shortest_path_to_bottom, we just add it to display it. This is case 1. (as in report) or second case as in problem stmnt
                path_edges = list(zip(shortest_path_to_bottom,shortest_path_to_bottom[1:]))
                nx.draw_networkx_edges(self.G,node_size=0.5,pos=pos,edgelist=path_edges,edge_color = 'green', width=2)
                continue
            
            # there is no path from any top vertex to any bottom vertex
            # so we compute the length of largest shortest path from vertex v and add it to display it.
            lengths = nx.single_source_dijkstra_path_length(self.G, u)  # get the length of the shortest path from node `u` to all other reachable nodes
            dest = max(lengths, key=lengths.get)                        # get the node with the longest path
            path = nx.dijkstra_path(self.G, u, dest)                    # get the actual longest path
            # print("path =",path)
            path_edges = list(zip(path,path[1:]))                       # get the edge lists
            # print("path_edges =",path_edges)
            nx.draw_networkx_edges(self.G,node_size=0.5,pos=pos,edgelist=path_edges,edge_color = 'green', width=2)
            
        # plt.savefig('.Q5_showpaths.png')
        plt.show()

    
l = Lattice(100)
l.show()
l.percolate(0.7)
l.show()
print(l.existsTopDownPath())

l.showPaths()