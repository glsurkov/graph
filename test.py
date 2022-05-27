import pandas as pd
import algorythms
import functions
import copy
import networkx as nx
from time import time


filename = input('Введите название файла( Пример: test.txt, text.csv ):  ')
separate = input('Введите разделитель в файлe (если разделитель - табуляция, то написать tab, если пробел - space):  ')
type_or = input('Введите тип графа (directed or undirected):   ')
format = filename[-4:]

if format == '.txt' or format =='.mtx':
    with open(filename,'r') as f:
        for i in range(1,4):
            f.readline()
        text = f.read()
else:
    with open(filename, 'r') as f:
        text = f.read()


filetxt = filename[:-4]


with open(filetxt + '-read.txt','w') as f:
    f.write(text)

# Класс для графа

class Graph:
    def __init__(self,filename):


        if separate != 'tab' and separate != 'space' and format != '.csv':
            df = pd.read_table(filename, sep=separate)
        elif separate == 'space':
            df = pd.read_table(filename, sep=' ')
        elif separate == ',' and format != '.csv':
            df = pd.read_table(filename, sep=separate)
        else:
            df = pd.read_table(filename)

        if format == '.txt' or format =='.mtx':
            df2 = df.drop_duplicates(subset=['FromNodeId'])['FromNodeId']
            df3 = df.drop_duplicates(subset=['ToNodeId'])['ToNodeId']
        else:
            df[['u', 'v', 't', 'h']] = df['u,v,t,h'].str.split(',', expand=True)
            df2 = df.drop_duplicates(subset=['u'])['u']
            df3 = df.drop_duplicates(subset=['v'])['v']

        resdf = sorted(list(set(list(df2.values) + list(df3.values))))


        graph = dict.fromkeys(resdf)
        edges = []
        for key in graph:
            graph[key] = set()
        if format == '.txt' or format == '.mtx':
            for node in df.values:
                edges.append(list(node))
                key = node[0]
                value = node[1]
                graph[key].add(value)
        else:
            for node in df[['u','v']].values:
                edges.append(list(node))
                key = node[0]
                value = node[1]
                graph[key].add(value)

        self.edges = edges
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
        return self.numberOfEdges()/((self.numberOfNodes()*(self.numberOfNodes() - 1))/2)

    # Неориентированный
    def undirect(self):
        undirect_graph = copy.deepcopy(self.graph)
        for key in self.graph:
            for value in self.graph[key]:
                    undirect_graph[value].add(key)

        return undirect_graph

    def reverse(self):
        reversed_graph = copy.deepcopy(self.graph)
        for key in self.graph.keys():
            if len(self.graph[key]) > 0:
                for value in self.graph[key]:
                    if key not in reversed_graph[value]:
                        reversed_graph[value].add(key)
                        reversed_graph[key].remove(value)

        return reversed_graph



g = Graph(filetxt + '-read.txt')
nxg = nx.read_edgelist(filetxt + '-read.txt')

print(g.numberOfNodes())
print(g.numberOfEdges())

# g_undirect = g.undirect()
#
# length = 0
# for key in g_undirect:
#     length = length + len(g_undirect[key])
#
# weak_components = functions.findWeakComponents(g_undirect)
# biggest_weak_component = functions.findMaxWeak(weak_components)
#
# numberNodes = g.numberOfNodes()
# graphDistance = functions.findGraphDistance(biggest_weak_component, g_undirect)
#
#
# if type_or == 'directed':
#     strong_components = algorythms.kosarai(g)
#     functions.metaGraph(strong_components['colors'], g.edges)
#     print('Количество ребер ор. в графе: ' + str(g.numberOfEdges()))
#     print('Количетсво компонент сильной связности: ' + str(len(strong_components['strong_comp'])))
#     print('Доля вершин в максимальной по мощности компоненте сильной связности: ' + str(functions.findMax(strong_components['strong_comp']) / numberNodes))
# print('Количество ребет в неор. графe: ' + str(length//2))
# print('Количество вершин в графе: ' + str(numberNodes))
# print('Плотность графа: ' + str(g.density()))
# print('Количество компонент слабой связности: ' + str(len(weak_components)))
# print('Доля вершин в максимальной по мощности компоненте слабой связности: ' + str(biggest_weak_component['length']/numberNodes))
# print('Радиус графа: ' + str(graphDistance['radius']) + '   Диаметр графа: ' + str(graphDistance['diametr']) + '   90-й процентиль: ' + str(graphDistance['percentile']))
#
#
# start = time()
# clusterCoefficients = functions.average_cluster_coefficient(g_undirect)
# print("Число треугольников (полных  подграфов  на 3 вершинах): ", clusterCoefficients['triangles'])
# print("Средний кластерный коэффициент: ", clusterCoefficients['averageCluster'])
# print("Глобальный кластерный коэффициент: ", clusterCoefficients['globalCluster'])
# end = time()
# print("Время работы моего решения: ", end - start, "секунд")
#
# start = time()
# print("Число треугольников (networkx): ", int(sum(nx.triangles(nxg).values()) / 3))
# print("Средний кластерный коэффициент (networkx): ", nx.average_clustering(nxg))
# print("Глобальный кластерный коэффициент (networkx): ", nx.transitivity(nxg))
# end = time()
# print("Время работы решения networkx: ", end - start, "секунд")
#
#
# degreeInfo = functions.nodeDegrees(g_undirect)
# print('Минимальная степень узла в графе: ', degreeInfo['minDegree'])
# print('Максимальная степень узла в графе: ', degreeInfo['maxDegree'])
# print('Средняя степень узла в графе: ', degreeInfo['avgDegree'])
# probabilityFunc = functions.degreeProbability(degreeInfo['degrees'],
#                                               degreeInfo['minDegree'],
#                                               degreeInfo['maxDegree'],
#                                               numberNodes)
# functions.showPlots(probabilityFunc)
#
# functions.delete_random_nodes(g_undirect)
# functions.delete_max_degree_nodes(g_undirect)
