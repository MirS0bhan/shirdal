import time

from threading import Thread, Lock, Condition

from .queue import AbstractQueue
from .container import Container


class TaskManager:
    def __init__(self, queue: AbstractQueue):
        self.tasks = queue  # Use deque for task queue
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def add_task(self, task: object) -> None:
        with self.condition:
            self.tasks.enqueue(task)
            self.condition.notify()  # Notify the executor that a task is available

    def get_task(self) -> object | None:
        with self.condition:
            while not self.tasks:
                self.condition.wait()  # Wait for a task to be added
            return self.tasks.dequeue()

    def purge(self) -> None:
        with self.lock:
            pass  # Clear all tasks


class TaskExecutor(Thread):
    def __init__(self, manager: TaskManager, container: Container):
        self.manager = manager
        self.container = container
        super().__init__()

    def run(self) -> None:
        while True:
            task = self.manager.get_task()
            func = self.container.resolve(task["endpoint"])
            try:
                func(task)  # Execute the task
            except Exception as e:
                print(f"Error executing task: {e}")
            #time.sleep(0.0001)  # Sleep to prevent busy waiting
