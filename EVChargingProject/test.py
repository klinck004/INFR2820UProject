

class priorityQueue:
    def __init__(self):
        self.queue = []

    def _heapify(self, size, i):
        smallest = i
        left_child_index = 2 * i + 1
        right_child_index = 2 * i + 2

        # Check if leftChildIndex is smaller than n to avoid IndexError and
        # if the left child is smaller than current element i, set smallest to left child
        if left_child_index < size and self.queue[left_child_index] < self.queue[smallest]:
            smallest = left_child_index

        # Check if leftChildIndex is smaller than n to avoid IndexError and
        # if the right child is smaller than the value in smallest, set smallest to right child
        if right_child_index < size and self.queue[right_child_index] < self.queue[smallest]:
            smallest = right_child_index

        # Termination condition: if the current element i and the smallest element are not equal, continue to heapify
        # if i and smallest are equal (smallest is the root node of the heap), then terminate
        if smallest != i:
            self.queue[i], self.queue[smallest] = self.queue[smallest], self.queue[i]
            self._heapify(size, smallest)

    def insert(self, num):
        size = len(self.queue)
        if size == 0: # If the array is empty, simply append the number to the array
            self.queue.append(num)
        else: # Otherwise append the number to the array and heapify the array
            self.queue.append(num)
            for i in range(size//2-1, -1, -1):
                self._heapify(size, i)

    def __str__(self):
        return str(self.queue)

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

newQueue = priorityQueue()
newQueue.insert(20)
newQueue.insert(3)
newQueue.insert(9)
newQueue.insert(4)
newQueue.insert(5)
newQueue.insert(18)
print(newQueue)
