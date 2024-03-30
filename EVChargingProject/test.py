import heapq


def dijkstra(graph, start, end):
    # Initialize distances
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Priority queue to store nodes with their distances
    pq = [(0, start)]

    while pq:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(pq)

        # Check if we have reached the destination
        if current_node == end:
            return distances[end]

        # Explore neighboring nodes
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            # Update distance if shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    # If end node is not reachable
    return float('inf')


# Given graph
graph = {
    'A': {'B': 6, 'F': 8},
    'B': {'A': 6, 'C': 5, 'G': 6},
    'C': {'B': 5, 'D': 7, 'H': 5},
    'D': {'C': 7, 'E': 7, 'I': 8},
    'E': {'D': 7, 'I': 6, 'N': 15},
    'F': {'G': 8, 'A': 5, 'J': 7},
    'G': {'F': 8, 'H': 9, 'K': 8, 'B': 6},
    'H': {'G': 9, 'I': 12, 'C': 5},
    'I': {'H': 12, 'D': 8, 'E': 6, 'M': 10},
    'J': {'K': 5, 'F': 7, 'O': 7},
    'K': {'L': 7, 'J': 5, 'G': 8},
    'L': {'K': 7, 'M': 7, 'P': 7},
    'M': {'L': 7, 'N': 9, 'I': 10},
    'N': {'M': 9, 'E': 15, 'R': 7},
    'O': {'P': 13, 'J': 7, 'S': 9},
    'P': {'Q': 8, 'O': 13, 'L': 7, 'U': 11},
    'Q': {'R': 9, 'P': 8},
    'R': {'Q': 9, 'N': 7, 'W': 10},
    'S': {'T': 9, 'O': 9},
    'T': {'U': 8, 'S': 9},
    'U': {'V': 8, 'P': 11, 'T': 8},
    'V': {'W': 5, 'U': 8},
    'W': {'V': 5, 'R': 10}
}

# Find the shortest path from A to W
shortest_distance = dijkstra(graph, 'M', 'W')
print("Shortest distance from A to W:", shortest_distance)
