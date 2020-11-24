graph1 = {
    'A' : ['B','S'],
    'B' : ['A'],
    'C' : ['D','E','F','S'],
    'D' : [],
    'E' : ['C','H'],
    'F' : ['C','G'],
    'G' : ['F','S'],
    'H' : ['E','G'],
    'S' : ['A','C','G']
}

def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n, visited)
    return visited


def printpath(node,visited,graph, path):
    if node not in visited:
        if node not in graph or graph[node] == []:
            print(path)
        else:
            visited.append(node)
            path.append(node)
            for x in graph[node]:
                printpath(x,visited,graph,path)

printpath('A',[],graph1,[])
