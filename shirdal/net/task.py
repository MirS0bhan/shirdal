from shirdal.core.queue import AbstractQueue
from .rpc import ServerRPC, ClientRPC

from threading import Thread

from shirdal.core.task import TaskManager


class ServerTaskManager(ServerRPC, TaskManager, Thread):
    def __init__(self, port, queue: AbstractQueue):
        ServerRPC.__init__(self, port)
        TaskManager.__init__(self, queue)
        Thread.__init__(self)

    def run(self):
        self._start_server()


class ClientTaskManager(ClientRPC, TaskManager):
    def __init__(self, host, port):
        ClientRPC.__init__(self, host, port)
        self.setup()

    def add_task(self, task: object) -> None:
        return self._call('add_task', task=task)
