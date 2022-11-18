import math
class Graph_num7:
    def __init__(self, size):
        self.size = size
        self.table = None

# size = int(input('Matrix MxM size: '))
# g  = Graph_num7(size)
# g.table = [([0]*size) for ran in range(size)]
# for i in range(0,size):
#     for j in range(i+1,size):
#         g.table[i][j]=int(input(f'{i} to{j}: '))
#         g.table[j][i]=g.table[i][j]
        
# print(g.table)

g  = Graph_num7(8) 
g.table = [[0, 1, 2, 3, 4, 5, 6, 7], 
           [1, 0, 5, 0, 15, 0, 0, 11], 
           [2, 5, 0, 7, 0, 4, 0, 0], 
           [3, 0, 7, 0, 9, 14, 23, 0], 
           [4, 15, 0, 9, 0, 10, 0, 0], 
           [5, 0, 4, 14, 10, 0, 2, 0], 
           [6, 0, 0, 23, 0, 2, 0, 1], 
           [7, 11, 0, 0, 0, 0, 1, 0]]

def minDistance(graph, distance, shortestTree):
    m = math.inf
    for v in range(graph.size):
        if distance[v] < m and shortestTree[v] == False:
            m = distance[v]
            minindex = v
    return minindex

def Dijkstra(graph, src_vertex):
    distance = [math.inf] * graph.size
    distance[src_vertex] = 0
    shortestTree = [False] * graph.size

    for i in range(graph.size):
        u = minDistance(graph, distance, shortestTree)

        shortestTree[u] = True

        for ver in range(graph.size):
            weight = graph.table[u][ver]
            if weight > 0 and shortestTree[ver] == False and distance[ver] > distance[u] + weight:
                distance[ver] = distance[u] + weight
    print("Vertex tDistance from Source")
    for n in range(graph.size):
        print(n, distance[n])

Dijkstra(g, 0)