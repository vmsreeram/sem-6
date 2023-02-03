import matplotlib.pyplot as plt
import random
import math

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

        plt.scatter(degree_count.keys(), [x/total for x in degree_count.values()],color='b',label='Actual degree distribution',s=3)
        plt.axvline(x=avgVal,color='r',label='Avg. node degree')
        plt.title('Node Degree Distribution')
        plt.xlabel('Node degree')
        plt.ylabel('Fraction of nodes')
        plt.grid()
        # plt.legend(bbox_to_anchor=(0.5, 1.075), loc='lower center', borderaxespad=0,ncol=2)     # use or not use?
        plt.legend()
        plt.show()
        
    """new code starts"""
    
    def isConnected(self):
        visited = [False for _ in range(self.n)]
        queue = []
        start = 1
        queue.append(start)
        visited[start-1] = True
        while queue:
            node = queue.pop(0)
            for n in self.adj_list[node]:
                if not visited[n-1]:
                    visited[n-1] = True
                    queue.append(n)
        return all(visited)     # all(iterable): Return True if bool(x) is True for all values x in the iterable. If the iterable is empty, return True.

    """new code ends"""
                

class ERRandomGraph(UndirectedGraph):
    def sample(self, p):
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                if random.random() < p:
                    self.addEdge(i, j)

def verify_er_connectivity(n):
    y = []
    for p in [i/n for i in range(1,100)]:
        sumresults = 0
        for i in range(1000):
            g = ERRandomGraph(n)
            g.sample(p)
            sumresults+=(g.isConnected())
        y.append(sumresults / 1000)
    plt.plot([i/n for i in range(1,100)],y,c='b')
    plt.axvline(x=math.log(n)/n,color='r',label='Theoretical threshold')
    plt.xlabel('p',style='italic')
    plt.ylabel('fraction of runs G({}, p) is connected'.format(n))
    plt.title('Connectedness of a G({}, p) as function of p'.format(n))
    plt.grid()
    plt.legend()
    plt.show()

verify_er_connectivity(100)


''' g = UndirectedGraph(5)
g = g + (1, 2)
g = g + (2, 3)
g = g + (3, 5)
print(g.isConnected())
print(g) '''