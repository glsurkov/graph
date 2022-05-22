import collections

# Поиск в ширину первая реализация
def bfs(graph,root,level, deleted_vertices=[]):
    level[root] = 0
    max_level = -1
    visited = set()
    edges = []
    queue = collections.deque([root])
    visited.add(root)
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in visited and neighbour not in deleted_vertices:
                level[neighbour] = level[vertex] + 1
                if level[neighbour] >= max_level:
                    max_level = level[neighbour]
                visited.add(neighbour)
                queue.append(neighbour)
    return {'nodes': list(visited), 'level': max_level}

# Поиск в ширину второая реализация
def bfs2(graph, i, random_nodes):

    unvisited = set(random_nodes)
    unvisited.discard(i)
    level = {i: 0}
    queue = collections.deque([(i,0)])
    while unvisited:
        v, path = queue.popleft()
        for w in graph[v]:
            if w not in level:
                queue.append((w, path + 1))
                level[w] = path + 1
                unvisited.discard(w)
    paths = {}
    for i in random_nodes:
        paths[i] = level[i]

    return paths
# Поиск в глубину
def dfs(graph,start,type,visited,tout,component = None,color = None,vertices = None):
        visited[start] = True
        stack = [start]
        if type == 'inverse':
            component.append(start)
            vertices[start] = color

        while stack:
            counter = 0
            u = stack[-1]
            if len(graph[u]) > 0:
                for i in sorted(graph[u]):
                    if not visited[i]:
                        stack.append(i)
                        visited[i] = True
                        if type == 'inverse':
                            vertices[i] = color
                            component.append(i)
                        break
                    else:
                        counter = counter + 1
                        if counter == len(graph[u]):
                            if type == 'direct':
                                tout.append(u)
                            stack.pop(-1)
            else:
                stack.pop(-1)
                if type == 'direct':
                    tout.append(u)

# Косарайю
def kosarai(g):
    net = g.graph
    vertices = {}
    reverse_net = g.reverse()
    strong_components = []
    tout = []
    visited = dict.fromkeys(net.keys(),False)
    for i in net.keys():
        if not visited[i]:
            dfs(net,i,'direct',visited,tout)
    for i in visited:
        visited[i] = False
    tout = tout[::-1]
    color = 0
    for i in tout:
        if not visited[i]:
            component = []
            dfs(reverse_net,i,'inverse',visited,tout,component,color,vertices)
            color = color + 1
            if len(component) > 0 :
                strong_components.append(component)
    return {'strong_comp' : strong_components, 'colors' : vertices}


# def floydWarshall(matrix, graph):
#     for k in graph:
#         for j in graph:
#             for i in graph:
#                 d = matrix[(i,k)] + matrix[(k,j)]
#                 if matrix[(i,j)] > d:
#                     matrix[(i,j)] = d
