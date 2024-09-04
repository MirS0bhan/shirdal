import threading
from collections import deque
from typing import Callable, Type
import time

from .queue import AbstractQueue, ListQueue


class TaskManager:
    def __init__(self, queue: Type[AbstractQueue]):
        self.tasks = queue()  # Use deque for task queue
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def add_task(self, task: Callable[[], None]) -> None:
        with self.condition:
            self.tasks.enqueue(task)
            self.condition.notify()  # Notify the executor that a task is available

    def get_task(self) -> Callable[[], None]:
        with self.condition:
            while not self.tasks:
                self.condition.wait()  # Wait for a task to be added
            return self.tasks.dequeue()

    def purge(self) -> None:
        with self.lock:
            pass  # Clear all tasks


class TaskExecutor:
    def __init__(self, manager: TaskManager):
        self.manager = manager
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()

    def run(self) -> None:
        while True:
            task = self.manager.get_task()
            try:
                task()  # Execute the task
            except Exception as e:
                print(f"Error executing task: {e}")
            time.sleep(0.0001)  # Sleep to prevent busy waiting


class Broker:
    def __init__(self, ):
        self.tm = TaskManager(ListQueue)
        self.te = TaskExecutor(self.tm)
