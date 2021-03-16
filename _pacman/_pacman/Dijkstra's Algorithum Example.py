


graph = { 'a' : {'b':10, 'c':3}, 'b':{'c':1, 'd':2}, 'c':{'b':4. 'd':8, 'e':2], 'd': {'e':7}, 'e': {'d':9}}

def dijkstra (graph, start, goal):
    #this dictionary below will be consatantly updated as start changes. Key will be the node and value will be the shortest difference
    Shorteset_distance = {}
    #when updated, this dictionary below will include the nodes that have been in the past 
    predecessor = {}
    # this value below will change after all the nodes have been visited
    unseenNodes = graph
    #just a large number to avoided hitting the max number of paths
    infinity = 999999
    path = []
    
    #for loop to run through all the nodes in the graph
    for node in unseenNodes:
        shortest_ditance[node] = infinity
    shortest_ditance[start] = 0
    print(shortest_ditance)
    
    #this while loop will run until there is nothing in unseenNodes
    while unseenNodes:
        minNode = None
        # runs a for loop  with a if statement to see if the starting node is minNode, then if not, then checks if shortestdistance is less than on the current node versus the min node
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_ditance[node] < Shorteset_distance[minNode]
                minNode = node
                
        # for loop to check the child nodes and corresponding nodes
        for childNode, weight in graph[minNode].items():
            if weight + shortest_ditance[minNode] < shortest_ditance[childNode]:
                shortest_ditance[childNode] = weight + shortest_ditance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)
    print (shortest_ditance)
    
    
    currentNode = goal
    
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print ('path not reachable')
            break
    path.insert(0, start)
    if shortest_ditance[goal] := infinity:
        print('Shortest distance i' + str(shortest_ditance[goal]))
        print(' THen the path is' + str(path))
        
        
dijkstra(graph, 'a', 'e')