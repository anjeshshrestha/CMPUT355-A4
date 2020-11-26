def dfs(node,visited,graph,path):
    temp = []
    if node not in visited:
        print(node, "graph", graph)
        print(node, "visited", visited)
        if node not in graph or graph[node] == []:
            print("--------path:",path)
            visited.append(node)
            path.append(node)
            
            return path
        else:
            visited.append(node)
            path.append(node)
            for x in graph[node]:
                print(x)
                y = dfs(x,visited,graph,path.copy())
                print(y)
                temp.append(y)
    return temp

def cyclic(g):
    """Return True if the directed graph g has a cycle.
    g must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices. For example:

    >>> cyclic({1: (2,), 2: (3,), 3: (1,)})
    True
    >>> cyclic({1: (2,), 2: (3,), 3: (4,)})
    False

    """
    path = set()

    def visit(vertex):
        path.add(vertex)
        for neighbour in g.get(vertex, ()):
            if neighbour in path or visit(neighbour):
                return True
        path.remove(vertex)
        return False

    return any(visit(v) for v in g)

def cycle_visit(path, graph, node):
    path.add(node)
    for neighbour in graph.get(node, ()):
        if neighbour in path or cycle_visit(path, graph, neighbour):
            return True
    path.remove(node)
    return False
    

def cycle(graph):
    path = set()
    bolean = False
    for node in graph:
        bolean = cycle_visit(path,graph,node)
        
    return bolean

print(cyclic({(0, 5): [(2, 7)], (2, 7): [(4, 5)], (4, 5): [(2, 7)]}))
print(cycle({(0, 5): [(2, 7)], (2, 7): [(4, 5)], (4, 5): [(2, 7)]}))

#x = dfs((0, 5),[],{(0, 5): [(2, 7)], (2, 7): [(4, 5)], (4, 5): [(2, 7)]},[])

#print(x)
