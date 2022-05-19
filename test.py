import pandas as pd
import algorythms
import functions
import copy
import networkx as nx
from time import time

with open('web-Google.txt','r') as f:
    for i in range(1,4):
        f.readline()
    text = f.read()

with open('read.txt','w') as f:
    f.write(text)

# Класс для графа

class Graph:
    def __init__(self, filename):
        df = pd.read_table(filename)
        df2 = df.drop_duplicates(subset=['# FromNodeId'])['# FromNodeId']
        df3 = df.drop_duplicates(subset=['ToNodeId'])['ToNodeId']

        resdf = list(set(list(df2.values) + list(df3.values)))
        graph = dict.fromkeys(resdf)
        for key in graph:
            graph[key] = set()

        for node in df.values:
            key = node[0]
            value = node[1]
            graph[key].add(value)

        self.graph = graph


    # Число вершин
    def numberOfNodes(self):
        return len(self.graph)

    # Число ребер
    def numberOfEdges(self):

        length = 0
        for key in self.graph:
            length = length + len(self.graph[key])
        return length

    # Плотность
    def density(self):
        return self.numberOfEdges()/(self.numberOfNodes()*(self.numberOfNodes() - 1))

    # Неориентированный
    def undirect(self):
        undirect_graph = copy.deepcopy(self.graph)
        for key in self.graph:
            for value in self.graph[key]:
                undirect_graph[value].add(key)

        return undirect_graph

    def reverse(self):
        reversed_graph = copy.deepcopy(self.graph)
        for key in self.graph:
            for value in self.graph[key]:
                reversed_graph[value].add(key)
                reversed_graph[key].remove(value)

        return reversed_graph


g = Graph('read.txt')
nxg = nx.read_edgelist('read.txt')


g_undirect = g.undirect()
weak_components = functions.findWeakComponents(g_undirect)
biggest_weak_component = functions.findMaxWeak(weak_components)


strong_components = algorythms.kosarai(g)
functions.metaGraph(strong_components,g.graph)
numberNodes = g.numberOfNodes()
graphDistance = functions.findGraphDistance(biggest_weak_component, g_undirect)


print('Количество ребер в графе: ' + str(g.numberOfEdges()))
print('Количество вершин в графе: ' + str(numberNodes))
print('Плотность графа: ' + str(g.density()))
print('Количество компонент слабой связности: ' + str(len(weak_components)))
print('Доля вершин в максимальной по мощности компоненте слабой связности: ' + str(biggest_weak_component['length']/numberNodes))
print('Количетсво компонент сильной связности: ' + str(len(strong_components)))
print('Доля вершин в максимальной по мощности компоненте сильной связности: ' + str(functions.findMax(strong_components)/numberNodes))
print('Радиус графа: ' + str(graphDistance['radius']) + '   Диаметр графа: ' + str(graphDistance['diametr']) + '   90-й процентиль: ' + str(graphDistance['percentile']))


start = time()
number_of_triangles, average_coefficient, global_coefficient = functions.average_cluster_coefficient(g_undirect)
print("Число треугольников (полных  подграфов  на 3 вершинах): ", number_of_triangles)
print("Средний кластерный коэффициент: ", average_coefficient)
print("Глобальный кластерный коэффициент: ", global_coefficient)
end = time()
print("Время работы моего решения: ", end - start, "секунд")

start = time()
print("Число треугольников (networkx): ", int(sum(nx.triangles(nxg).values()) / 3))
print("Средний кластерный коэффициент (networkx): ", nx.average_clustering(nxg))
print("Глобальный кластерный коэффициент (networkx): ", nx.transitivity(nxg))
end = time()
print("Время работы решения networkx: ", end - start, "секунд")
