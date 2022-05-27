import landmarks


# бфс, строящий дерево кратчайших путей
def bfsLandmarkSPT(graph, i, level):
    SPT = dict({i: None})  # для вершины хранит предка
    level[i] = 0
    queue = [i]
    while queue:
        v = queue.pop(0)
        for w in graph[v]:
            if level[w] == -1:
                queue.append(w)
                level[w] = level[v] + 1
                SPT[w] = v
    return SPT


# найти путь от landmark до i
def getPath(SPT, i):
    path = [i]
    current = i
    while SPT[current] is not None:
        path.insert(0, SPT[current])
        current = SPT[current]
    return path


# вычисляет расстояние между вершинами s и t для одного landmark
def distanceLCA(graph, landmark, s, t):
    level = dict.fromkeys(graph.keys(), -1)
    SPT = bfsLandmarkSPT(graph, landmark, level)
    level.clear()

    path1 = getPath(SPT, s)
    path2 = getPath(SPT, t)

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

    minDist = None
    for v in vertices:
        dist = distanceLCA(graph, v, s, t)
        if (minDist is None) or (dist < minDist):
            minDist = dist

    return minDist
