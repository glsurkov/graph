import collections

# Поиск в ширину
def bfs(graph, root,level):
    level[root] = 0
    max_level = -1
    visited = set()
    edges = []
    queue = collections.deque([root])
    visited.add(root)
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                level[neighbour] = level[vertex] + 1
                if level[neighbour] >= max_level:
                    max_level = level[neighbour]
                visited.add(neighbour)
                queue.append(neighbour)
    return {'nodes': list(visited), 'level': max_level}

# Поиск в глубину
def dfs(graph,start,type,visited,tout,component = None):
    visited[start] = True
    stack = [start]
    if type == 'inverse':
        component.append(start)
    else:
        tout.append(start)
    while stack:
        counter = 0
        u = stack[-1]
        if len(graph[u]) > 0:
            for i in sorted(graph[u]):
                if not visited[i]:
                    stack.append(i)
                    visited[i] = True
                    if type == 'inverse':
                        component.append(i)
                    else:
                        tout.append(i)
                    break
                else:
                    counter = counter + 1
                    if counter == len(graph[u]):
                        stack.pop(-1)
        else:
            stack.pop(-1)

# Косарайю
def kosarai(g):
    net = g.graph
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
    for i in tout:
        if not visited[i]:
            component = []
            dfs(reverse_net,i,'inverse',visited,tout,component)
            if component != None:
                strong_components.append(component)
    return strong_components


def floydWarshall(matrix, graph):
    for k in graph:
        for j in graph:
            for i in graph:
                d = matrix[(i,k)] + matrix[(k,j)]
                if matrix[(i,j)] > d:
                    matrix[(i,j)] = d
