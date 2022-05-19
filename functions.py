import algorythms
import collections
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import math

# Функция, находящая компоненты слабой связности(на вход подается неориентированный граф)
def findWeakComponents(graph):
    level = dict.fromkeys(graph, -1)
    weak_components = []

    for number in level:
        if level[number] == -1:
            weak_components.append(algorythms.bfs(graph, number,level))

    return weak_components

def findMaxWeak(list):
    maximum = -1

    for i in list:
        if len(i['nodes']) > maximum:
            maximum = len(i['nodes'])
            maximum_nodes = i['nodes']

    return {'length': maximum, 'nodes': maximum_nodes}

def findMax(list):
    maximum = -1

    for i in list:
        if len(i) > maximum:
            maximum = len(i)

    return maximum

def graphDistance(random_nodes,e):
    radius = float('inf')
    diametr = -1
    for i in random_nodes:
        radius = min(radius,e[i])
        diametr = max(diametr,e[i])
    return {'radius': radius, 'diametr': diametr}


def eccentricity(random_nodes,matrix,e):
    for i in random_nodes:
        for j in random_nodes:
            e[i] = max(e[i],matrix[(i,j)])


def percentile(random_nodes, matrix):
    distance = list()
    for i in sorted(random_nodes):
        for j in sorted(random_nodes):
            if(i > j):
                distance.append(matrix[(i,j)])
    value = sorted(distance)[round((90*len(distance))/100) - 1]
    return value



def findGraphDistance(component,graph):
    matrix = collections.defaultdict(int)
    e = collections.defaultdict(int)
    edges = []
    for i in component['nodes']:
        for j in component['nodes']:
            if j in graph[i]:
                edges.append([i,j])
    random_nodes = random.sample(component['nodes'], 6)


    for i in component['nodes']:
        e[i] = 0
        for j in component['nodes']:
            if int(i) == int(j):
                matrix[(i, j)] = 0
                continue
            for k in edges:
                if int(i) == k[0] and int(j) == k[1]:
                    matrix[(i, j)] = 1
                    break
            if matrix[(i, j)] == 0:
                matrix[(i, j)] = float('inf')


    algorythms.floydWarshall(matrix,component['nodes'])
    eccentricity(random_nodes,matrix,e)
    graph_distance = graphDistance(random_nodes,e)
    value = percentile(random_nodes,matrix)
    graph_distance['percentile'] = value

    return graph_distance


def metaGraph(strong_components, graph):

    metaGraph = nx.DiGraph()

    for i in range(0,len(strong_components)):
        for j in range(0,len(strong_components)):
            if i != j:
                for node1 in strong_components[i]:
                    for node2 in strong_components[j]:
                        if node2 in graph[node1]:
                            metaGraph.add_edge(i,j)
                            break
                    if metaGraph.has_edge(i, j):
                        break
        if not metaGraph.has_node(i):
            metaGraph.add_node(i)


    nx.draw(metaGraph)
    plt.show()

# Функция вычисляющая число треугольников, средний и глобальный кластерные коэффициенты
def average_cluster_coefficient(graph):
    average_cluster = 0
    triangles = 0
    global_cluster_numerator = 0
    global_cluster_denominator = 0
    for key in graph:
        edges = 0
        if len(graph[key]) < 2:
            local_cluster = 0
        else:
            neighbour_union = Counter()
            for v in graph[key]:
                neighbour_union += Counter(graph[v])
            for v in graph[key]:
                edges += neighbour_union[v]
            edges /= 2
            triangles += edges
            local_cluster = 2 * edges / (len(graph[key]) * (len(graph[key]) - 1))
        global_cluster_numerator += local_cluster * math.comb(len(graph[key]), 2)
        global_cluster_denominator += math.comb(len(graph[key]), 2)
        average_cluster += local_cluster
    average_cluster /= len(graph)
    triangles /= 3
    global_cluster = global_cluster_numerator / global_cluster_denominator
    return int(triangles), average_cluster, global_cluster
