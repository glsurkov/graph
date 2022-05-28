import landmarks
import collections


# бфс, строящий дерево кратчайших путей
def bfsLandmarkSPT(graph, i, level):
    SPT = dict({i: None})  # для вершины хранит предка
    level[i] = 0
    queue = collections.deque()
    queue.append(i)
    while queue:
        v = queue.popleft()
        for w in graph[v]:
            if w not in level:
                queue.append(w)
                level[w] = level[v] + 1
                SPT[w] = v
    return SPT


# найти путь от landmark до i
def getPath(SPT, i):
    path = [i]
    current = i
    if current not in SPT:
        return float('inf')
    while SPT[current] is not None:
        path.insert(0, SPT[current])
        current = SPT[current]
    return path


# вычисляет расстояние между вершинами s и t для одного landmark
def distanceLCA(graph, landmark, s, t, level):
    SPT = bfsLandmarkSPT(graph, landmark, level)
    level.clear()

    path1 = getPath(SPT, s)
    if path1 == float('inf'):
        return float('inf')
    path2 = getPath(SPT, t)
    if path2 == float('inf'):
        return float('inf')

    i = LCA = 0

    while (i < len(path1)) and (i < len(path2)):
        if path1[i] == path2[i]:
            LCA = i
        i = i + 1

    dist1 = len(path1) - LCA - 1
    dist2 = len(path2) - LCA - 1

    return dist1 + dist2


# LCA модификация
def LandmarksLCA(graph, k, s, t, type):
    if type == 'degree':
        vertices = landmarks.highDegree(graph, k)
    elif type == 'coverage':
        M = k + k // 3
        vertices = landmarks.bestCoverage(graph, k, M)
    else:
        vertices = landmarks.randomLandmarks(graph, k)

    minDist = float('inf')

    for v in vertices:
        level = dict()
        dist = distanceLCA(graph, v, s, t, level)
        if dist < minDist:
            minDist = dist

    return minDist
