import algorythms
import random
import networkx as nx
import matplotlib.pyplot as plt


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
