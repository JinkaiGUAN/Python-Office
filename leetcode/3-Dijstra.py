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
from typing import Dict, Mapping, Tuple

graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}  # The number in the dictionary represents the weight of the edge


def initialize_distance(graph: Dict, s: str) -> Dict:
    """Initiliaze the distance dictionary, i.e., mapping the node to total distance.
    The start point with weight of 0, others are all assigned to infnity.

    Args:
        graph (Dict): The graph.
        s (str): Start point.

    Returns:
        Dict: Contains node name and their weights.
    """
    distance = {s: 0}
    for vertex in graph:
        if vertex != s:
            distance[vertex] = math.inf
    return distance


def dijkstra(graph: Dict, s: str = 'A') -> Tuple[Dict, Dict]:
    """Dijkstra algorithm.

    Args:
        graph (Dict): The graph.
        s (str): Start point.

    Returns:
        Tuple[Dict, Dict]: parent and distance dictionaries. Parent dictionary give the previouse node of the current
         node, in the presence of the minimum weight.
    """
    pqueue = []
    heapq.heappush(pqueue, (0, s))  # priority queue
    seen = set()
    parent = {s: None}
    distance = initialize_distance(graph, s)

    while (len(pqueue) > 0):
        dist, vertex = heapq.heappop(pqueue)
        seen.add(vertex) # only we pop out the vertex, we cay say we visited this vertex.

        # neighbour_nodes = graph[vertex].keys()
        for neighbour in graph[vertex].keys():
            if not neighbour in seen:
                if (dist + graph[vertex][neighbour]) < distance[neighbour]:
                    heapq.heappush(pqueue, (dist + graph[vertex][neighbour], neighbour))
                    parent[neighbour] = vertex
                    distance[neighbour] = dist + graph[vertex][neighbour]
    
    return parent, distance


def draw_route(parent: Dict, end: str = 'F') -> str:
    """Draw the route.

    Args:
        parent (Dict): Parent dictionary give the previouse node of the current
         node, in the presence of the minimum weight.
        end (str, optional): The end point. Defaults to 'F'.

    Returns:
        str: Route.
    """
    def draw_route_helper(parent: Dict, end: str = 'F') -> str:
        if not parent[end]:
            return end
        else:
            return end + ' <- ' + draw_route_helper(parent, parent[end]) 
    
    return draw_route_helper(parent, end)[::-1].replace('<', '>')


def main():
    parent, distance = dijkstra(graph, 'A')
    print(parent)
    print(distance)
    print(draw_route(parent, 'F'))


if __name__ == "__main__":
    main()


