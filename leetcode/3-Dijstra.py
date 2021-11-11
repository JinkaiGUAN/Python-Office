# graph = {
#     'A': ['B', 'C'],
#     'B': ['A', 'C', 'D'],
#     'C': ['A', 'B', 'D', 'E'],
#     'D': ['B', 'C', 'E', 'F'],
#     'E': ['C', 'D'],
#     'F': ['D']
# }
import heapq
import math

graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}  # The number in the dictionary represents the weight of the edge

def initialize_distance(graph, s):
    distance = {s: 0}
    for vertex in graph:
        if vertex != s:
            distance[vertex] = math.inf
    return distance

def dijkstra(graph, s):
    pqueue = []
    heapq.heappush(pqueue, (0, s))  # priority queue
    seen = set()
    parent = {s: None}
    distance = initialize_distance(graph, s)

    while (len(pqueue) > 0):
        dist, vertex = heapq.heappop(pqueue)
        print(dist, vertex)
        seen.add(vertex)

        # neighbour_nodes = graph[vertex].keys()
        for neighbour in graph[vertex].keys():
            if not neighbour in seen:
                if (dist + graph[vertex][neighbour]) < distance[neighbour]:
                    print((dist + graph[vertex][neighbour], neighbour))
                    heapq.heappush(pqueue, (dist + graph[vertex][neighbour], neighbour))
                    parent[neighbour] = vertex
                    distance[neighbour] = dist + graph[vertex][neighbour]
    
    return parent, distance


parent, distance = dijkstra(graph, 'A')
print(parent)
print(distance)
