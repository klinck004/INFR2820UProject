# Priority queue
class priorityQueue:
    def __init__(self):
        self.queue = []
    def _heapify(self, size, i):
        # self.queue: array, size: size of array, index of current element -- starting at first non-leaf node with index of n/2 - 1
        # Set current element i as smallest
        size = len(self.queue)

        smallest = i
        leftChildIndex = 2 * i  # Index of the left child of current element i
        rightChildIndex = 2 * i + 1 # Index of the right child of current element i

        # Check if leftChildIndex is smaller than n to avoid IndexError and
        # if the left child is smaller than current element i, set smallest to left child
        if leftChildIndex < size and self.queue[leftChildIndex] < self.queue[smallest]:
            smallest = leftChildIndex

        # Check if leftChildIndex is smaller than n to avoid IndexError and
        # if the right child is smaller than the value in smallest, set smallest to right child
        if rightChildIndex < size and self.queue[rightChildIndex] < self.queue[smallest]:
            smallest = rightChildIndex

        # Termination condition: if the current element i and the smallest element are not equal, continue to heapify
        # if i and smallest are equal (smallest is the root node of the heap), then terminate
        if smallest != i:
            self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[i] # Swap smallest with the current element i
            self._heapify(size, smallest) # Recursion -- heapify the array again

    def insert(self, entry):
        size = len(self.queue)
        if size == 0: # If the array is empty, simply append the number to the array
            self.queue.append(entry)
        else: # Otherwise append the number to the array and heapify the array
            self.queue.append(entry)
            for i in range(size//2-1, -1, -1):
                self._heapify(size, i)

    def delete(self, vertex):
        size = len(self.queue)
        result = -1
        i = 0
        # Search if the vertex exists in the heap
        for i in range(0, size):
            if ((self.queue[i])[1] == vertex):
                result = i  # Return the index of the vertex if it does

        if result == -1:  # If result = -1 (vertex not found in heap), raise error
            print("Not found in queue")
        else:
            # Swap element to be deleted with last element
            self.queue[result], self.queue[size - 1] = self.queue[size - 1], self.queue[result]
            # Remove last element
            self.queue.pop(size-1)

            for x in range(size // 2 - 1, -1, -1):
                # Iterate over each non-leaf node in the heap starting at the index of the last non-leaf node (n/2-1) as heapifying starts there
                # and moving backwards to the root node
                self._heapify(size, x)
    def empty(self):
        if len (self.queue) == 0: return True
        else: return False

    def getMin(self):
        return self.queue[0]

    def pop(self):
        self.delete((self.getMin())[1])

    def __str__(self):
        return str(self.queue)

# Load graph
graph = {
    # Layer 1
    'A' : {'B': 6, 'F': 8},
    'B' : {'A': 6, 'C': 5, 'G': 6},
    'C' : {'B': 5, 'D': 7, 'H': 5},
    'D' : {'C': 7, 'E': 7, 'I': 8},
    'E' : {'D': 7, 'I': 6, 'N': 15},
    # Layer 2
    'F' : {'G': 8, 'A': 5, 'J': 7},
    'G' : {'F': 8, 'H': 9, 'K': 8, 'B': 6},
    'H' : {'G': 9, 'I': 12, 'C': 5},
    'I' : {'H': 12, 'D': 8, 'E': 6, 'M': 10},
    # Layer 3
    'J' : {'K': 5, 'F': 7, 'O': 7},
    'K' : {'L': 7, 'J': 5, 'G': 8},
    'L' : {'K': 7, 'M': 7, 'P': 7},
    'M' : {'L': 7, 'N': 9, 'I': 10},
    'N' : {'M': 9, 'E': 15, 'R': 7},
    # Layer 4
    'O' : {'P': 13, 'J': 7, 'S': 9},
    'P' : {'Q': 8, 'O': 13, 'L': 7, 'U': 11},
    'Q' : {'R': 9, 'P': 8},
    'R' : {'Q': 9, 'N': 7, 'W': 10},
    # Layer 5
    'S' : {'T': 9, 'O': 9},
    'T' : {'U': 8, 'S': 9},
    'U' : {'V': 8, 'P': 11, 'T': 8},
    'V' : {'W': 5, 'U': 8},
    'W' : {'V': 5, 'R': 10}
}


# Dijkstra's Algorithm
def dijkstra(G, S):
    distance = {}  # Dictionary storing the tentative distances from start node S to all other nodes in graph
    previous = {}  # Dictionary storing the preceding node for each node along the shortest path from start node S
    visited = set()

    Q = priorityQueue()
    #print(distances)

    # Initialization
    for vertex in G:
        distance[vertex] = float('inf')
        previous[vertex] = None
    distance[S] = 0
    Q.insert((distance[S], S)) # Add starting node to the priority queue

    while not Q.empty():
        print("Nodes to visit:", Q.queue)
        current = Q.getMin() # Get the node with the smallest distance in the priority queue
        currentStr = current[1]
        currentDist = current[0]
        print ("-------------")
        print(f"Shortest distance in queue: {currentStr}, {currentDist}")
        print ("Selecting:", currentStr)
        print(f"Added {currentStr} to visited list")
        print ("---")

        visited.add(currentStr) # Add current node to visited list
        Q.pop() # Remove node from priority queue
        for neighbor in G[currentStr]: # Find the neighbours of the current node from the graph
            print (f"Adjacent to {currentStr}: {neighbor}")
            if neighbor not in visited: # For each unvisited neighbour V of U
                print (f"   {neighbor} is NOT VISITED. Distance from {currentStr}: {G[currentStr][neighbor]}")
                print (f"   Current recorded distance for {neighbor}: {distance[neighbor]}")
                tempDistance = currentDist + G[currentStr][neighbor]  # tempDistance
                print(f"   Distance from start node {S} via {currentStr}: {tempDistance}")

                if tempDistance < distance[neighbor]:
                    print(f"    UPDATE:")
                    print(f"        {tempDistance} is less than current recorded distance {distance[neighbor]}")
                    print(f"        Added {neighbor} to queue")
                    distance[neighbor] = tempDistance
                    previous[neighbor] = currentStr
                    Q.delete(neighbor)
                    Q.insert((distance[neighbor], neighbor))
                else:
                    print(f"    NO CHANGE:")
                    print(f"        {tempDistance} is greater than current recorded distance {distance[neighbor]}")
                    print(f"        NO CHANGE: {distance[neighbor]} is still shortest distance")


            else:
                print(f"    {neighbor} is already visited")
        print("---")
        print("")

    print("Distance", distance)
    print("Previous", previous)
    print(Q)
    #G - graph containing vertices, edges, and weights
    #S - source/start node
    #Q - priority queue
    #U - current node
    #V - unvisited node adjacent to current node U

dijkstra(graph, 'A')
