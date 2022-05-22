import algorythms
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import math


# Функция, находящая компоненты слабой связности(на вход подается неориентированный граф)
def findWeakComponents(graph, deleted_vertices=[]):
    level = dict.fromkeys(graph, -1)
    weak_components = []

    for number in level:
        if level[number] == -1 and number not in deleted_vertices:
            weak_components.append(algorythms.bfs(graph, number,level, deleted_vertices))

    return weak_components

def findMaxWeak(list):
    maximum = -1
    maximum_nodes = []

    for i in list:
        if len(i['nodes']) > maximum:
            maximum = len(i['nodes'])
            maximum_nodes = i['nodes']

    return {'length': maximum if maximum >= 0 else 0, 'nodes': maximum_nodes}

def findMax(list):
    maximum = -1

    for i in list:
        if len(i) > maximum:
            maximum = len(i)

    return maximum

def precompute(graph,random_nodes):
    paths = dict.fromkeys(random_nodes)


    for i in random_nodes:
                path = algorythms.bfs2(graph,i,random_nodes)
                paths[i] = path
    return paths

def graphDistance(random_nodes,e):
    radius = float('inf')
    diametr = -1

    for i in random_nodes:
        radius = min(radius,e[i])
        diametr = max(diametr,e[i])

    return {'radius': radius, 'diametr': diametr}

def eccentricity(random_nodes,paths,e):
    for i in random_nodes:
        for j in random_nodes:
            if i != j:
                e[i] = max(e[i],paths[i][j])

def percentile(random_nodes, rasst):

    distance = list()
    for i in sorted(random_nodes):
        for j in sorted(random_nodes):
            if(j > i):
                distance.append(rasst[i][j])
    value = sorted(distance)[round((90*len(distance))/100) - 1]

    return value



def findGraphDistance(component, graph):

    comp = dict.fromkeys(component['nodes'])
    for i in comp:
        comp[i] = set()
    for i in component['nodes']:
        for j in graph[i]:
                comp[i].add(j)

    random_nodes = random.sample(component['nodes'], 500)
    e = dict.fromkeys(random_nodes,0)

    rasst = precompute(comp,random_nodes)

    eccentricity(random_nodes,rasst,e)

    graph_distance = graphDistance(random_nodes,e)
    value = percentile(random_nodes,rasst)
    graph_distance['percentile'] = value

    return graph_distance


def metaGraph(colors, edges):

    metaGraph = nx.DiGraph()

    for edge in edges:
        if colors[edge[0]] != colors[edge[1]]:
            metaGraph.add_edge(colors[edge[0]],colors[edge[1]])


    plt.figure(1,figsize = (65, 65))
    pos = nx.random_layout(metaGraph)
    nx.draw(metaGraph, pos = pos, node_size = 5, width = 0.2, arrowsize = 3)
    plt.show()

# Функция, вычисляющая число треугольников, средний и глобальный кластерные коэффициенты
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
    return {'triangles': int(triangles), 'averageCluster': average_cluster, 'globalCluster': global_cluster}

def nodeDegrees(graph):  # на вход неориентированный граф (?)
    degrees = dict()
    min = max = avg = -1
    sum = 0

    for key in graph:
        degree = len(graph[key])
        degrees[degree] = degrees[degree] + 1 if degree in degrees else 1

        if (min == -1) or (degree < min):
            min = degree
        if degree > max:
            max = degree
        sum += degree

    avg = sum / len(graph)
    return {'degrees': degrees, 'minDegree': min, 'maxDegree': max, 'avgDegree': avg}

def degreeProbability(degrees, min, max, nodes_amount):  # возвращает функцию вероятности для степени вершины
    x = list(range(min, max + 1))
    y = [degrees[degree] / nodes_amount if degree in degrees else 0 for degree in x]
    return {'x': x, 'y': y}

def showPlots(probabilityFunc):
    x = probabilityFunc['x']
    y = probabilityFunc['y']

    plt.plot(x, y)
    plt.title("probability of degree for node (linear)")
    plt.xlabel('degree')
    plt.ylabel('probability')
    #plt.savefig('linear.png')
    plt.show()

    plt.bar(x, y)
    plt.title("probability of degree for node (hist)")
    plt.xlabel('degree')
    plt.ylabel('probability')
    #plt.savefig('hist.png')
    plt.show()

    plt.plot(x, y)
    plt.title("probability of degree for node (log-log)")
    plt.xlabel('degree')
    plt.ylabel('probability')
    plt.xscale('log')
    plt.yscale('log')
    #plt.savefig('loglog.png')
    plt.show()

# Функция, удаляющая некоторый процент узлов в графе и вычисляюща долю вершин в максимальной компоненте слабой связности
def delete_random_nodes(graph):
    deleted_vertices = []
    rand_percent_number = random.randrange(101)  # генерация процента удаляемых узлов
    number_of_vertices = len(graph)
    deleted_vertices = random.sample(range(0, number_of_vertices),
                                     round(number_of_vertices * rand_percent_number / 100))
    print('Удаляется ', rand_percent_number, '% узлов: ', deleted_vertices)
    weak_components = findWeakComponents(graph, deleted_vertices)
    biggest_weak_component = findMaxWeak(weak_components)
    print('Максимальная компонента слабой связности: ', biggest_weak_component['nodes'])
    print('Доля вершин в максимальной по мощности компоненте слабой связности: ' +
          str(biggest_weak_component['length'] / number_of_vertices))


def get_nodes_with_max_degree(graph, max):
    list_of_vertices = []
    for key in graph:
        if (len(graph[key]) == max):
            list_of_vertices.append(key)
    return list_of_vertices


# Функция, возвращающая rand_number случайных вершин из списка
def get_random_vertices_from_list(list_of_vertices, rand_number):
    number_of_vertices = random.sample(range(0, len(list_of_vertices)), rand_number)
    random_vertices_from_list = []
    for i in number_of_vertices:
        random_vertices_from_list.append(list_of_vertices[i])
    return random_vertices_from_list


# Функция, удаляющая некоторый процент узлов максимальной степени в графе и вычисляюща долю вершин в максимальной компоненте слабой связности
def delete_max_degree_nodes(graph):
    deleted_vertices = []
    degreeInfo = nodeDegrees(graph)
    nodes_of_max_degree = get_nodes_with_max_degree(graph, degreeInfo['maxDegree'])
    print('Узлы максимальной степени ', nodes_of_max_degree)
    rand_percent_number = random.randrange(101)  # генерация процента удаляемых узлов
    number_of_vertices = len(graph)
    deleted_vertices = get_random_vertices_from_list(nodes_of_max_degree, round(
        len(nodes_of_max_degree) * rand_percent_number / 100))
    print('Удаляется ', rand_percent_number, '% узлов максимальной степени: ', deleted_vertices)
    weak_components = findWeakComponents(graph, deleted_vertices)
    biggest_weak_component = findMaxWeak(weak_components)
    print('Максимальная компонента слабой связности: ', biggest_weak_component['nodes'])
    print('Доля вершин в максимальной по мощности компоненте слабой связности: ' +
          str(biggest_weak_component['length'] / number_of_vertices))
