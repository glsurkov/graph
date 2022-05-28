import random
import networkx as nx
import landmarks
import copy
import pandas as pd
import time


# имя файла с датасэтом
import landmarksLCA

filename = input('Введите название файла( Пример: test.txt, text.csv ):  ')
# разделитель между ребрами в файле
separate = input('Введите разделитель в файлe (если разделитель - табуляция, то написать tab, если пробел - space):  ')
# тип выбора вершин
type_of_landmarks = input('Введите метод выбора вершин (coverage, degree, random) :  ')
k = input('Введите кол-во landmarks: ')

format = filename[-4:]


if format == '.txt' or format == '.mtx':
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


if separate != 'tab' and separate != 'space' and format != '.csv' :
    df = pd.read_table(filetxt + '-read.txt', sep=separate)
elif separate == 'space':
    df = pd.read_table(filetxt + '-read.txt', sep=' ')
elif separate == ',':
    df = pd.read_table(filetxt + '-read.txt', sep = ',')
else:
    df = pd.read_table(filetxt + '-read.txt')


gr = nx.Graph()


for edge in df.values:
    gr.add_edge(int(edge[0]),int(edge[1]))


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

        if format == '.txt' or format == '.mtx':
            df2 = df.drop_duplicates(subset=['FromNodeId'])['FromNodeId']
            df3 = df.drop_duplicates(subset=['ToNodeId'])['ToNodeId']
        else:
            df[['u', 'v']] = df['node_1,node_2'].str.split(',', expand=True)
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
        for key in self.graph.keys():
            if len(self.graph[key]) > 0:
                for value in self.graph[key]:
                    if key not in reversed_graph[value]:
                        reversed_graph[value].add(key)
                        reversed_graph[key].remove(value)

        return reversed_graph


g = Graph(filetxt + '-read.txt')
g_undirect = g.undirect()

# стартовая вершина
start_v = random.choice(list(g_undirect.keys()))
# конечная вершина
end_v = random.choice(list(g_undirect.keys()))


print('Начальная вершина: ' + str(start_v) + '  Конечная вершина: ' + str(end_v))

start = time.time()
if type_of_landmarks == 'coverage':
    M = int(k) + int(k)//4
    landmarks.bestCoverage(g_undirect,int(k),M)
elif type_of_landmarks == 'degree':
    landmarks.highDegree(g_undirect,int(k))
else:
    landmarks.randomLandmarks(g_undirect,int(k))
print('Время ' + type_of_landmarks + ' : ' + str(time.time() - start))

# networkX считает расстояние
start = time.time()
nX_path = nx.shortest_path_length(gr,int(start_v),int(end_v))
print('Расстояние NetworkX: ' + str(nX_path))
print('Время NetworkX: ' + str(time.time() - start))


# Подсчет нашего расстояния
start = time.time()
my_path = 0
for i in range(0, 5):
    my_path = my_path + landmarks.landmarksBasic(g_undirect,int(k),start_v,end_v,type_of_landmarks)

print('Время вычисления расстояния: ' + str((time.time() - start)/5))

print('Наше расстояние: ' + str(my_path/5))
print('Погрешность   ' + str(abs(my_path/5 - nX_path)))


# Подсчет расстояния по Landmarks-LCA
print()
print("### Landmarks-LCA ###")
start = time.time()
my_path_LCA = 0
for i in range(0, 5):
    my_path_LCA = my_path_LCA + landmarksLCA.LandmarksLCA(g_undirect,int(k),start_v,end_v,type_of_landmarks)

print('Время вычисления расстояния: ' + str((time.time() - start)/5))

print('Наше расстояние по LCA: ' + str(my_path_LCA/5))
print('Погрешность   ' + str(abs(my_path_LCA/5 - nX_path)))