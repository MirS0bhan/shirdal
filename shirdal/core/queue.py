from abc import ABC, abstractmethod


class AbstractQueue(ABC):
    @abstractmethod
    def enqueue(self, item):
        """Add an item to the end of the queue."""
        pass

    @abstractmethod
    def dequeue(self):
        """Remove and return the item from the front of the queue."""
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Return True if the queue is empty, False otherwise."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items in the queue."""
        pass

    @abstractmethod
    def peek(self):
        """Return the item at the front of the queue without removing it."""
        pass


class ListQueue(AbstractQueue):
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        return len(self) == 0

    def __len__(self):
        return len(self.queue)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self.queue[0]

