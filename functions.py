import algorythms
import collections
import random

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
    print(matrix)
    for i in random_nodes:
        for j in random_nodes:
            e[i] = max(e[i],matrix[(i,j)])


def findGraphDistance(component,graph):
    matrix = collections.defaultdict(int)
    e = collections.defaultdict(int)
    edges = []
    for i in component['nodes']:
        for j in component['nodes']:
            if j in graph[i]:
                edges.append([i,j])
    random_nodes = random.sample(component['nodes'], 500)


# def percentile()


    for i in component['nodes']:
        e[i] = 0
        for j in component['nodes']:
            if int(i) == int(j):
                matrix[(i, j)] = 0
                continue
            for k in edges:
                if int(i) == k[0] and int(j) == k[1]:
                    matrix[(i, j)] = 1
                    matrix[(j, i)] = 1
                    break
            if matrix[(i, j)] == 0:
                matrix[(i, j)] = float('inf')

    algorythms.floydWarshall(random_nodes,matrix,component['nodes'])
    eccentricity(random_nodes,matrix,e)
    graph_distance = graphDistance(random_nodes,e)

    return graph_distance
