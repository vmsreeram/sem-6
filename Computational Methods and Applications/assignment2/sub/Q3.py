import matplotlib.pyplot as plt
import random
import math
import tqdm

class UndirectedGraph:
    def __init__(self, n=None):
        if n is not None and ((type(n)!=int) or n<0):   # disallowing user to initialise with anything other than non-neg int
            raise Exception("Invalid initialisation: only a non-negative integer is allowed")
        self.n = n
        self.adj_list = {}                              # implemented as dict. Key is added whenever a node is added to UndirectedGraph, with value being an empty list, denoting the neighbouring nodes to the node corresponding to the key.
        if n:                                           # if n is specified, we add nodes from 1 to n
            for i in range(n):
                self.adj_list[i+1] = []

    def addNode(self, node):
        # We check if `node` passed is valid or not.
        if (type(node)!=int) or (node<=0):
            raise Exception("Invalid node addition: only a positive integer is allowed")
        if self.n and node > self.n:
            raise Exception("Node index cannot exceed number of nodes")
        
        # We update the adj_list if the node is not already added.
        if node not in self.adj_list:
            self.adj_list[node] = []
    
    def addEdge(self, a, b):
        if a==b:
            raise Exception("Self edges are not allowed!")
        # add node if not already added
        self.addNode(a)
        self.addNode(b)
        
        # connecting both ways, as it is an undirected graph. No multi edges are allowed.
        if self.adj_list[a].count(b)==0:
            self.adj_list[a].append(b)
        if self.adj_list[b].count(a)==0:
            self.adj_list[b].append(a)

    def __add__(self, other):                           # to allow the using of `+` operator
        if type(other) == tuple:
            self.addEdge(*other)
            return self
        elif type(other) == int:
            self.addNode(other)
            return self
        else:
            raise TypeError('Expected tuple or integer')

    def __str__(self):                                  # to allow printing of objects
        edges = 0
        for node in self.adj_list:
            edges += len(self.adj_list[node])
        edges = edges // 2                              # number of edges will be half of total number of end points of all edges
        
        res = "Graph with {} nodes and {} edges. Neighbours of the nodes are belows:".format(len(self.adj_list), edges)
        for node in self.adj_list:
            res += "\nNode {}: {{{}}}".format(node, ", ".join(str(x) for x in self.adj_list[node]))
        return res

    def plotDegDist(self):
        # since we plot degree from 0 to maximum possible degree corresponding to number of nodes in the graph, we compute Maxdegree
        total=len(self.adj_list)
        Maxdegree=total-1
        degree_count = {}                               # stores the number of nodes with each degree from 0...Maxdegree
        
        for i in range(Maxdegree+1):
            degree_count[i] = 0
        
        for node in self.adj_list:
            degree = len(self.adj_list[node])
            degree_count[degree] += 1

        # print(degree_count)
        # print("total =",total)
        
        # computing average node degree which is the average of degrees of each node
        avgVal=0
        for x in degree_count:
            avgVal += x*degree_count[x]/total

        plt.scatter(degree_count.keys(), [x/total for x in degree_count.values()],color='b',label='Actual degree distribution')
        plt.axvline(x=avgVal,color='r',label='Avg. node degree')
        plt.title('Node Degree Distribution')
        plt.xlabel('Node degree')
        plt.ylabel('Fraction of nodes')
        plt.grid()
        # plt.legend(bbox_to_anchor=(0.5, 1.075), loc='lower center', borderaxespad=0,ncol=2)     # use or not use?
        plt.legend()
        plt.show()
        
    """new code starts"""
    
    def isConnected(self):                      # performs breadth-first-search to check if the graph is connected or not
        
        # Null graph is vacuously connected
        if len(self.adj_list)==0:
            return True
        
        # perform bfs
        visited = [False for _ in range(self.n)]
        queue = []                              # act as exploration list
        start = 1                               # can start from any arbitrary vertex
        queue.append(start)
        visited[start-1] = True
        while queue:
            node = queue.pop(0)
            for n in self.adj_list[node]:       # for each n in neighbors of node
                if not visited[n-1]:            # if n isn't explored, add to exploration list (queue)
                    visited[n-1] = True
                    queue.append(n)
        return all(visited)                     # all(iterable): Return True if bool(x) is True for all values x in the iterable. If the iterable is empty, return True.

    """new code ends"""
                

class ERRandomGraph(UndirectedGraph):
    def sample(self, p):
        if type(self.n) is not int or self.n<0:                 # checking if the graph has fixed number of vertices.
            raise Exception("ERRandomGraph needs to be initialised with non-negative integer")
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                if random.random() < p:
                    self.addEdge(i, j)                          # add edge if sampled prob is less than sampling prob


def verify_er_connectivity():
    n=100
    y = []
    X = [i/1000 for i in range(101)]            # so that i runs from 0 to 100
    for p in tqdm.tqdm(X):                      # tqdm presents a progress bar which shows how much has been computed, howmuch is left.
        sumresults = 0
        for i in range(1000):
            g = ERRandomGraph(n)
            g.sample(p)
            sumresults+=(g.isConnected())
        y.append(sumresults / 1000)             # average of 1000 runs is of interest
    plt.plot(X,y,c='b')
    plt.axvline(x=math.log(n)/n,color='r',label='Theoretical threshold')
    plt.xlabel('p',style='italic')
    plt.ylabel('fraction of runs G({}, p) is connected'.format(n))
    plt.title('Connectedness of a G({}, p) as function of p'.format(n))
    plt.grid()
    plt.ylim(0,1)
    plt.legend()
    plt.show()
    # plt.savefig('.Q3_2.png')

verify_er_connectivity()
# g=UndirectedGraph(0)
# print(g.isConnected())

''' g = UndirectedGraph(5)
g = g + (1, 2)
g = g + (2, 3)
g = g + (3, 5)
print(g.isConnected())
print(g) '''