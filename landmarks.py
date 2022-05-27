import random
import time


# степень вершины
def degree(graph):
    degrees = dict.fromkeys(graph,0)
    for i in graph.keys():
        degrees[i] = len(graph[i])
    return degrees


# выбирает вершины с наибольшими степенями
def highDegree(graph, k):
    degrees = list(degree(graph).items())
    degrees.sort(reverse = True,key=lambda i: i[1])
    value = []
    for i in range(0,k):
        value.append(degrees[i][0])

    return value

# вершины с наилучшим покрытием
def bestCoverage(graph,k,M):
    paths = []
    keys = list(graph.keys())
    for i in range(0,M):
        s = random.choices(keys, k=2)
        res = bfsBestCoverage(graph,s)
        if res != None:
            paths.append(res)

    landmarks = []

    for i in range(0,k):
        vertices = []

        for j in range(0,len(paths)):
            vertices = vertices + paths[j]

        allV = set(vertices)
        maximumV = None
        maximum = 0

        for v in allV:
            k = vertices.count(v)
            if k > maximum:
                maximumV = v
                maximum = k
        if maximumV != None:
            landmarks.append(maximumV)


        for l in paths:
            if maximumV in l:
                paths.remove(l)

    return landmarks


# рандомные вершины
def randomLandmarks(graph, k):
    vertices = list(graph.keys())
    random_v = random.choices(vertices, k = k)

    return random_v


# бфс для налиучшего покрытия
def bfsBestCoverage(graph,s):
    unvisited = dict.fromkeys(graph.keys(), -1)
    father = dict.fromkeys(graph.keys(), None)
    queue = [s[0]]
    unvisited[s[0]] = 1
    path = []

    while queue:
        v = queue.pop(0)
        for w in graph[v]:
            if unvisited[w] == -1:
                queue.append(w)
                father[w] = v
                unvisited[w] = 1
                if w == s[1]:
                    path.append(w)
                    while v != None:
                        path.append(v)
                        v = father[v]
                    return path


# бфс для Landmarks-basic
def bfsLandmark(graph, i, paths, level):
    paths[i][i] = 0
    level[i] = 0
    queue = [i]
    while queue:
        v = queue.pop(0)
        for w in graph[v]:
            if level[w] == -1:
                queue.append(w)
                level[w] = level[v] + 1
                paths[i][w] = level[w]


# предвычислении расстояний между вершинами графа и landmarks
def precomputeLandmark(graph,k,type):
    if type == 'degree':
        vertices = highDegree(graph,k)
    elif type == 'coverage':
        M = k + k//3
        vertices = bestCoverage(graph,k,M)
    else:
        vertices = randomLandmarks(graph,k)


    paths = dict.fromkeys(vertices)
    for i in paths:
        paths[i] = dict()
    for i in vertices:
        level = dict.fromkeys(graph.keys(), -1)
        bfsLandmark(graph,i,paths,level)
        for v in level:
            if level[v] == -1:
                paths[i][v] = float('inf')
        level.clear()
    return paths


# базовый алгос
def landmarksBasic(graph,k,s,t,type):
    paths = precomputeLandmark(graph,k,type)
    d = float('inf')
    if s == t:
        return 0
    for i in paths:
            d = min(d,paths[i][s]+paths[i][t])
    return d