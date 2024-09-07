from typing import Union, Callable

from .broker import Broker


class Application:
    def __init__(self, brk: type[Broker]):
        self.broker = brk

    def service(self, item: Union[object, Callable]) -> Union[object, Callable]:
        """Decorator to register a service in the container."""
        self.broker.task_executor.container.register(item)
        return item  # Return the original item

    def operate(self, dt):
        """ Find endpoint and run it """
        self.broker.task_manager.add_task(dt)
