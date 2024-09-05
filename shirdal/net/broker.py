from shirdal.core.broker import Broker, TaskExecutor
from shirdal.core.queue import ListQueue
import threading
from shirdal.core.container import Container

from .task import ServerTaskManager, ClientTaskManager


class ServerBroker(Broker):
    def __init__(self, endpoint):
        self.co = Container()
        self.tm = ServerTaskManager(endpoint, ListQueue())
        self.te = TaskExecutor(self.tm, self.co)
        thread = threading.Thread(target=self.tm.start)
        thread.start()  # Start the thread


class ClientBroker(Broker):
    def __init__(self, endpoint):
        self.tm = ClientTaskManager(endpoint)
