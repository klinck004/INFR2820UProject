# Priority queue
class priorityQueue:
    def __init__(self):
        self.queue = []
    def _heapify(self, size, i):
        # self.queue: array, size: size of array, index of current element -- starting at first non-leaf node with index of n/2 - 1
        # Set current element i as smallest
        smallest = i
        leftChildIndex = 2 * i + 1 # Index of the right child of current element i
        rightChildIndex = 2 * i + 2 # Index of the left child of current element i

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
    def insert(self, num):
        size = len(self.queue)
        if size == 0: # If the array is empty, simply append the number to the array
            self.queue.append(num)
        else: # Otherwise append the number to the array and heapify the array
            self.queue.append(num)
            for i in range(size//2-1, -1, -1):
                self._heapify(size, i)
    def delete(self, num):
        size = len(self.queue)
        i = 0
        # Search if the number exists in the heap
        for i in range(0, size):
            if (self.queue[i] == num):
                result = i  # Return the index of the number if it does
        result = -1  # Return -1 if not

        if result == -1:  # If result = -1 (number not found in heap), raise error
            print("Not found in heap")
        else:
            # Swap element to be deleted with last element
            self.queue[i], self.queue[size - 1] = self.queue[size - 1], self.queue[i]
            # Remove last element
            self.queue.remove(num)
            for i in range(size // 2 - 1, -1, -1):
                # Iterate over each non-leaf node in the heap starting at the index of the last non-leaf node (n/2-1) as heapifying starts there
                # and moving backwards to the root node
                self._heapify(size, i)
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
    distance = []  # Array storing the tentative distances from start node S to all other nodes in graph
    previous = []  # Array storing the preceding node for each node along the shortest path from start node S
    visited = []

    Q = priorityQueue()
    distances = {vertex: float('inf') for vertex in graph}
    print(distances)
    # Initialization
    for vertex, (key, value) in enumerate(G.items()):
        # print(vertex, key)
        distance.insert(vertex, float('inf'))
        previous.insert(vertex, None)
        # Set distance of vertex to infinity
        # Set previous vertex to None
        if key == S:  # Set distance of start vertex to 0
            distance[vertex] = 0
            Q.insert((distance[vertex], key))
        #if key != S:  # If vertex is not equal to source node S, add vertex to priority queue
            #Q.insert((distance[vertex], key))

    print(distance)
    print(Q.queue[0][0])
    for vertex, (key, value) in enumerate(G.items()):
        print(key)
        for neighbor, weight in value.items():
            print(distances[neighbor], neighbor, weight)
            tempDistance = distances[key] + weight
            print(tempDistance)



    # While queue is not empty
    #while len(Q) != 0:

    '''
    for vertex, (key, value) in enumerate(G.items()):
        print("Node " + str(key))
        for test, (key, value) in enumerate(value.items()): # For each neighbouring node V of the current node
            if value not in visited:
                print("Not visited")
                print(key, value)
                print("Distance", distance[vertex])
                tempDistance = distance[vertex] + value
                print(tempDistance)
                if tempDistance < distance[vertex]:
                    distance[vertex] = tempDistance
                    previous[vertex] = value
                visited.append(value)
                Q.delete(value)
    '''




    # print(distance)



dijkstra(graph, 'A')