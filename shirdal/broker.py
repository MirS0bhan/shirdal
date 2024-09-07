from enum   import Enum, auto
from typing import Callable, Dict, Optional

from shirdal.core import TaskExecutor, Container, ListQueue, TaskManager
from shirdal.net  import ServerTaskManager, ClientTaskManager


class BrokerType(Enum):
    LOCAL = auto()
    SERVER = auto()
    CLIENT = auto()


class Broker:
    def __init__(self, task_manager: TaskManager, task_executor: Optional[TaskExecutor] = None):
        self.task_manager = task_manager
        self.task_executor = task_executor

    def start(self):
        if self.task_executor:
            self.task_executor.start()
            if hasattr(self.task_manager, 'start'):
                self.task_manager.start()

    def stop(self):
        if self.task_executor:
            self.task_manager.stop()
            self.task_executor.stop()

    def publish(self, topic: str, message: str):
        if isinstance(self.task_manager, TaskManager):
            self.task_manager.publish(topic, message)
        else:
            # Implement publish logic for server and client brokers
            pass

    def subscribe(self, topic: str, callback: Callable[[str], None]):
        if isinstance(self.task_manager, TaskManager):
            self.task_manager.subscribe(topic, callback)
        else:
            # Implement subscribe logic for server and client brokers
            pass

    @staticmethod
    def create(broker_type: BrokerType, host=None, port=6985) -> 'Broker':
        match broker_type:
            case BrokerType.LOCAL:
                container = Container()
                task_manager = TaskManager(ListQueue())
                task_executor = TaskExecutor(task_manager, container)
                return Broker(task_manager, task_executor)

            case BrokerType.SERVER:
                container = Container()
                task_manager = ServerTaskManager(port, ListQueue())
                task_executor = TaskExecutor(task_manager, container)
                return Broker(task_manager, task_executor)

            case BrokerType.CLIENT:
                task_manager = ClientTaskManager(host, port)
                return Broker(task_manager)

            case _:
                raise ValueError(f"Unknown broker type: {broker_type}")


class BrokerManager:
    def __init__(self):
        self.brokers: Dict[str, Broker] = {}

    def create_broker(self, name: str, broker_type: BrokerType, endpoint: Optional[str] = None) -> Broker:
        broker = Broker.create(broker_type, endpoint)
        self.brokers[name] = broker
        return broker

    def get_broker(self, name: str) -> Broker:
        return self.brokers.get(name)

    def start_all(self):
        for broker in self.brokers.values():
            broker.start()

    def stop_all(self):
        for broker in self.brokers.values():
            broker.stop()

    def publish(self, name: str, topic: str, message: str):
        broker = self.get_broker(name)
        if broker:
            broker.publish(topic, message)
        else:
            raise ValueError(f"Broker not found: {name}")

    def subscribe(self, name: str, topic: str, callback: Callable[[str], None]):
        broker = self.get_broker(name)
        if broker:
            broker.subscribe(topic, callback)
        else:
            raise ValueError(f"Broker not found: {name}")
