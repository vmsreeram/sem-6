import matplotlib.pyplot as plt
class UndirectedGraph:
    def __init__(self, n=None):
        self.n = n
        self.adj_list = {}
        if n:
            for i in range(1, n+1):
                self.adj_list[i] = []

    def addNode(self, node):
        if (type(node)!=int) or (node<=0):
            raise Exception("Invalid node addition: only a positive integer is allowed")
        if self.n and node > self.n:
            raise Exception("Node index cannot exceed number of nodes")
        if node not in self.adj_list:
            self.adj_list[node] = []
    
    def addEdge(self, a, b):
        self.addNode(a)
        self.addNode(b)
        self.adj_list[a].append(b)
        self.adj_list[b].append(a)

    def __add__(self, other):
        if type(other) == tuple:
            self.addEdge(*other)
            return self
        elif type(other) == int:
            self.addNode(other)
            return self

    def __str__(self):
        edges = 0
        for node in self.adj_list:
            edges += len(self.adj_list[node])
        edges = edges // 2
        res = "Graph with {} nodes and {} edges. Neighbours of the nodes are belows:".format(len(self.adj_list), edges)
        for node in self.adj_list:
            res += "\nNode {}: {{{}}}".format(node, ", ".join(str(x) for x in self.adj_list[node]))
        return res

    def plotDegDist(self):
        total=len(self.adj_list)
        degree_count = {}
        Maxdegree=total-1
        
        for i in range(1,Maxdegree+1):
            degree_count[i] = 0
        
        for node in self.adj_list:
            degree = len(self.adj_list[node])
            if degree in degree_count:
                degree_count[degree] += 1
            else:
                degree_count[degree] = 1
        # print(degree_count)
        # print("total =",total)
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
print(g)