# INFR2820U - EV Charging Station Route Optimization Application
# Group 32: Keenan Linck 100874397
# March 30th, 2024

# --------------------------------------------------------
# Verbose debug logging output
# Shows full step by step output for Dijkstra's algorithm
# True: Show output, False: No output
question = None
while question is None:
    question = input("Would you like to show full debug output for Dijkstra's algorithm? (Y/N): ")
    if question.lower() == "y":
        verbose = True
    elif question.lower() == "n":
        verbose = False
    else:
        print("Please enter a valid input (Y/N)")
        question = None

if verbose == True:
    print("***** DEBUG OUTPUT: ******")


def debug(message):
    if verbose == True:
        print(message)


# 1. Graph Construction and Data Loading
# Load graph
graph = {
    # Layer 1
    'A': {'B': 6, 'F': 8},
    'B': {'A': 6, 'C': 5, 'G': 6},
    'C': {'B': 5, 'D': 7, 'H': 5},
    'D': {'C': 7, 'E': 7, 'I': 8},
    'E': {'D': 7, 'I': 6, 'N': 15},
    # Layer 2
    'F': {'G': 8, 'A': 5, 'J': 7},
    'G': {'F': 8, 'H': 9, 'K': 8, 'B': 6},
    'H': {'G': 9, 'I': 12, 'C': 5},
    'I': {'H': 12, 'D': 8, 'E': 6, 'M': 10},
    # Layer 3
    'J': {'K': 5, 'F': 7, 'O': 7},
    'K': {'L': 7, 'J': 5, 'G': 8},
    'L': {'K': 7, 'M': 7, 'P': 7},
    'M': {'L': 7, 'N': 9, 'I': 10},
    'N': {'M': 9, 'E': 15, 'R': 7},
    # Layer 4
    'O': {'P': 13, 'J': 7, 'S': 9},
    'P': {'Q': 8, 'O': 13, 'L': 7, 'U': 11},
    'Q': {'R': 9, 'P': 8},
    'R': {'Q': 9, 'N': 7, 'W': 10},
    # Layer 5
    'S': {'T': 9, 'O': 9},
    'T': {'U': 8, 'S': 9},
    'U': {'V': 8, 'P': 11, 'T': 8},
    'V': {'W': 5, 'U': 8},
    'W': {'V': 5, 'R': 10}
}


# 2. Routing Algorithm Implementation
# Priority Queue
class priorityQueue:
    def __init__(self):
        # Initialize self.queue as a list
        self.queue = []

    def _heapify(self, size, i):
        # Inputs: self.queue: array, size: size of array, index of current element -- starting at first non-leaf node with index of n/2 - 1
        # Set current element i as smallest
        size = len(self.queue)

        # Set smallest to the index of current element (i)
        smallest = i
        leftChildIndex = 2 * i  # Index of the left child of current element i
        rightChildIndex = 2 * i + 1  # Index of the right child of current element i

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
            self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[
                i]  # Swap smallest with the current element i
            self._heapify(size, smallest)  # Recursion -- heapify the array again

    # Insert entry into priority queue
    def insert(self, entry):
        # Inputs: entry - tuple of (distance, vertex)
        size = len(self.queue)
        if size == 0:  # If the array is empty, simply append the entry to the array
            self.queue.append(entry)
        else:  # Otherwise append the entry to the array and heapify the array
            self.queue.append(entry)
            for i in range(size // 2 - 1, -1, -1):
                self._heapify(size, i)

    # Remove entry from priority queue
    def delete(self, vertex):
        # Inputs: vertex - string of vertex to be removed
        size = len(self.queue)
        result = -1
        i = 0
        # Search if the vertex exists in the heap
        for i in range(0, size):
            if ((self.queue[i])[1] == vertex):
                result = i  # Return the index of the vertex if it does

        if result == -1:  # If result = -1 (vertex not found in heap), do not delete and return debug message
            debug("No such vertex in queue")
        else:
            # Swap element to be deleted with last element
            self.queue[result], self.queue[size - 1] = self.queue[size - 1], self.queue[result]
            # Remove last element
            self.queue.pop(size - 1)

            # Iterate over each non-leaf node in the heap starting at the index of the last non-leaf node (n/2-1) as heapifying starts there
            # and moving backwards to the root node
            for x in range(size // 2 - 1, -1, -1):
                self._heapify(size, x)

    # If priority queue is empty, return that it is empty
    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    # Return element with lowest distance from the queue (index 0)
    def getMin(self):
        return self.queue[0]

    # Delete the element at the front of the queue
    def pop(self):
        self.delete((self.getMin())[1])

    # For debugging: simply return the queue variable as a string
    def __str__(self):
        return str(self.queue)


# Dijkstra's Algorithm
def dijkstra(G, S):
    # Variables used:
    # G - graph containing vertices, edges, and weights
    # S - source/start node
    # Q - priority queue
    # current (U) - current node
    # currentStr - the current node as a string
    # currentDist - the distance for the current node stored in the priority queue
    # neighbor (V) - unvisited node adjacent to current node U
    # distance[neighbor] - the distance currently stored in the distance dictionary for neighbouring node V
    # tempDistance - the temporary distance from the start node S to the neighbouring node

    distance = {}  # Dictionary storing the tentative distances from start node S to all other nodes in graph
    previous = {}  # Dictionary storing the preceding node for each node along the shortest path from start node S
    visited = set()  # Set storing visited nodes

    Q = priorityQueue()  # Priority queue (as defined above) to hold nodes and the current shortest distance

    # 1. Initialization
    # Iterate through each vertex V in graph G
    for vertex in G:
        distance[vertex] = float('inf')  # Assign infinity to vertex to indicate distance has yet to be calculated
        previous[vertex] = None  # Assign none to vertex to indicate path has not yet been found

    distance[S] = 0  # Set the distance of the start node to 0,
    Q.insert((distance[S], S))  # Add starting node to the priority queue to initiate algorithm

    # 2. Graph iteration
    while not Q.empty():  # While priority queue Q is not empty

        debug(f"Nodes to visit: {Q.queue}")
        current = Q.getMin()  # Get the node with the smallest distance in the priority queue (U)
        currentStr = current[1]  # Access the node as a string from the tuple
        currentDist = current[0]  # Access the distance for the node stored in the priority queue from the tuple

        # Console output
        debug("-------------")
        debug(f"Shortest distance in queue: {currentStr}, {currentDist}")
        debug(f"Selecting: {currentStr}")
        debug(f"Added {currentStr} to visited list")
        debug("---")

        visited.add(currentStr)  # Add current node to visited list
        Q.pop()  # Remove node from priority queue

        # Find the neighbours of the current node from the graph
        for neighbor in G[currentStr]:
            debug(f"Adjacent to {currentStr}: {neighbor}")
            if neighbor not in visited:  # For each unvisited neighbour V of U
                debug(f"   {neighbor} is NOT VISITED. Distance from {currentStr}: {G[currentStr][neighbor]}")
                debug(f"   Current recorded distance for {neighbor}: {distance[neighbor]}")

                # Calculate the temporary distance from the start node S to the neighbouring node by
                # adding the current distance of the node in the priority queue (Q) and the distance
                # between the current node U and the neighbouring node V
                tempDistance = currentDist + G[currentStr][neighbor]

                debug(f"   Distance from start node {S} via {currentStr}: {tempDistance}")

                # If the temporary distance (tempDistance) is less than the current distance recorded in distance (distance[neighbour]) for the neighbouring node V
                # Add the neighbouring node (V) to the priority queue (Q) for visitation, and
                # update the distance with the new distance and indicate the current node U as the node preceding the neighbouring node V
                if tempDistance < distance[neighbor]:
                    debug(f"    UPDATE:")
                    debug(f"        {tempDistance} is less than current recorded distance {distance[neighbor]}")
                    debug(f"        Added {neighbor} to queue")
                    distance[neighbor] = tempDistance
                    previous[neighbor] = currentStr
                    Q.delete(neighbor)
                    Q.insert((distance[neighbor], neighbor))

                # If the temporary distance (tempDistance) is greater than the current distance
                # recorded in distance (distance[neighbour]) for the neighbouring node V,
                # do not update the distance or insert the node into the priority queue (Q)

                else:
                    # Console output only
                    debug(f"    NO CHANGE:")
                    debug(f"        {tempDistance} is greater than current recorded distance {distance[neighbor]}")
                    debug(f"        NO CHANGE: {distance[neighbor]} is still shortest distance")

            # If the neighbour V of the current node U is already visited, print this output to the console
            else:
                # Console output only
                debug(f"    {neighbor} is already visited")
        debug("---")
        debug("")

    # Debug console output
    debug(f"Distance {distance}")
    debug(f"Previous {previous}")
    debug("End of Djikstra's Algorithm")
    debug("----------------------------------")
    # Return distance and previous dictionaries
    return distance, previous


# 3. Route Recommendation System
# Create a stack data structure for use in printing out the suggested route
class stack:
    def __init__(self):
        # Initialize self.stack as a list
        self.stack = []

    def isEmpty(self):
        # Return True if length of stack is 0, False otherwise
        return len(self.stack) == 0

    def push(self, item):
        # Append item to end (top) of stack
        self.stack.append(item)

    def pop(self):
        if self.isEmpty():  # If stack is empty, return that it is empty
            return "Stack is empty"
        return self.stack.pop()  # If stack is not empty, pop the item from the end (top) of the stack

    def __str__(self):
        # For displaying the array in reverse order
        # Top of stack - left, bottom of stack - right
        reversedOut = self.stack
        reversedOut.reverse()
        return str(reversedOut)

# Call Dijkstra's algorithm to calculate the shortest path from start point (S)
# Return the most efficient routes from the start point to the charging stations

def main():
    # Allow user to input starting node (S)
    startInput = None
    startPoint = None
    while startInput is None:
        startInput = input("Input the starting node to calculate distances (Leave blank for default: A): ")
        if len(startInput) != 0 and len(startInput) == 1 and startInput.isalpha():
            startPoint = startInput.upper()
            debug(startPoint)
        elif len(startInput) > 0 and startInput.isalpha() != True:
            print("Please enter a valid input (a single letter of the alphabet):")
            startInput = None
        elif len(startInput) == 0:
            print("Using default starting node A")
            startPoint = 'A'
        else:
            print("Error: Please try again.")

    # Variable definitions:
    chargStations = ['H', 'K', 'Q', 'T']  # Locations of charging stations
    routing = dijkstra(graph, startPoint)  # Call algorithm to calculate path

    distances = routing[0]  # Distances from start point to each node in the graph
    previousNodes = routing[1]  # The shortest path from start point to each node in the graph

    # Route recommendation console output
    print("")
    print(f"Fastest routes from {startPoint} to Charging Station:")
    print("-----")
    for node, distance in distances.items():  # Iterate through the nodes and their distances from the start node (S) from the calculated distances in distances
        if node in chargStations:  # If the node is a charging station
            route = stack()  # Use stack to hold route
            vertex = node
            print(f"{startPoint} to Charging Station {node}: {distance}")
            route.push(vertex)  # Push charging station node to start reverse traversal of previous nodes
            while previousNodes[vertex] != None:
                prev = previousNodes[vertex]  # Get previous node of input node
                route.push(prev)  # Push previous node to route stack
                vertex = prev  # Set vertex to previous node to get the previous node of that node
            # Print the shortest route from start node to charging station
            route.stack.reverse()
            length = len(route.stack)
            for x in range(length):
                if x != length - 1:
                    print(f"{route.stack[x]}", end=" -> ")
                else:
                    print(f"{route.stack[x]}")
            print("-----")


# Run program
if __name__ == "__main__":
    main()
