import matplotlib.pyplot as plt
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

g = UndirectedGraph()
# g = g + 100
# g = g + (1, 2)
# g = g + (1, 100)
# g = g + (100, 3)
# g = g + 20
g += (1,1)
print(g)
g.plotDegDist()