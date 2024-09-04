from typing import Union, Callable

from .core import Container, Broker


class Application:
    def __init__(self):
        self.container = Container()
        self.broker = Broker()

    def service(self, item: Union[object, Callable]) -> Union[object, Callable]:
        """Decorator to register a service in the container."""
        self.container.register(item)
        return item  # Return the original item

    def operate(self, dt):
        """ Find endpoint and run it """
        endpoint = dt.endpoint
        f = self.container.resolve(endpoint)
        self.broker.tm.add_task(lambda: f(dt))
