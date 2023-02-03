import matplotlib.pyplot as plt
import random
import math
import tqdm

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

    """new code starts"""
    
    def oneTwoComponentSizes(self):
        visited = set()
        nodes = list(self.adj_list.keys())
        ans = [0, 0]
        for node in nodes:
            if node not in visited:
                size = self.__bfs_size(node, visited)
                if size > ans[0]:
                    ans[1] = ans[0]
                    ans[0] = size
                elif size > ans[1]:
                    ans[1] = size
        return ans

    def __bfs_size(self, start, visited):
        queue = [start]
        size = 0
        while queue:
            node = queue.pop(0)
            if node not in visited:
                size += 1
                visited.add(node)
                neighbours = self.adj_list[node]
                queue.extend(neighbours)
        return size
    
    """new code ends"""
                

class ERRandomGraph(UndirectedGraph):
    def sample(self, p):
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                if random.random() < p:
                    self.addEdge(i, j)

# g = ERRandomGraph(100)
# g.sample(0.01)
# # print(g)
# print(g.oneTwoComponentSizes())

def verify_er_one_two_connectivity():
    n=1000
    y_lar = []
    y_2nd = []
    X = [i*0.0001 for i in range(0,90)]
    for p in tqdm.tqdm(X):
        sumresults_lar = 0
        sumresults_2nd = 0
        for _ in range(50):
            g = ERRandomGraph(n)
            g.sample(p)
            ans = g.oneTwoComponentSizes()
            sumresults_lar+=(ans[0])/n
            sumresults_2nd+=(ans[1])/n
        y_lar.append(sumresults_lar / 50)
        y_2nd.append(sumresults_2nd / 50)
    
    plt.plot(X,y_lar,c='g',label='Largest connected component')
    plt.plot(X,y_2nd,c='b',label='2nd largest connected component')
    plt.axvline(x=1/n,color='r',label='Largest CC size threshold')
    plt.axvline(x=math.log(n)/n,color='orange',label='Connectedness threshold')
    plt.xlabel('p',style='italic')
    plt.title('Fraction of nodes in the largest and second-largest\nconnected components (CC) of G({}, p) as function of p'.format(n))
    plt.ylabel('fraction of nodes'.format(n))
    plt.grid()
    plt.legend()
    plt.show()
    # plt.savefig('.Q4_2.png')

verify_er_one_two_connectivity()
