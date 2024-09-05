from shirdal.core.queue import AbstractQueue
from .rpc import ServerRPC, ClientRPC


from shirdal.core.broker import TaskManager


class ServerTaskManager(ServerRPC, TaskManager):
    def __init__(self, endpoint, queue: AbstractQueue):
        ServerRPC.__init__(self, endpoint)
        TaskManager.__init__(self, queue)


class ClientTaskManager(ClientRPC, TaskManager):
    def __init__(self, endpoint):
        ClientRPC.__init__(self, endpoint)

    def add_task(self, task: object) -> None:
        return self._call('add_task', task=task)
