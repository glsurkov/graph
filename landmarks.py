def degree(graph):
    degrees = dict.fromkeys(graph,0)
    for i in graph.keys():
        degrees[i] = degrees[i] + len(graph[i])
        for j in graph[i]:
            degrees[j] = degrees[j] + 1
    print(degrees)
    return degrees



def selectLandmarks(graph, k):
    degrees = list(degree(graph).items())
    degrees.sort(reverse = True,key=lambda i: i[1])
    print(degrees)
    value = []
    for i in range(0,k):
        value.append(degrees[i][0])

    return value


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

def precomputeLandmark(graph,k):
    vertices = selectLandmarks(graph,k)
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


def landmarksBasic(graph,k,s,t):
    paths = precomputeLandmark(graph,k)
    print(paths)
    d = float('inf')
    if s == t:
        return 0
    for i in paths:
            d = min(d,paths[i][s]+paths[i][t])
    return d