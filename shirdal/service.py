from typing import Callable, Union

from pydantic import TypeAdapter

from .core.container import ContainerAbstract
from .utils import get_methods, get_type_list, get_name


class ServiceContainer(ContainerAbstract):
    def __init__(self):
        self.registry = {}

    async def resolve(self, name: str):
        for a in self.registry.get(name.__class__):
            yield a

    def register(self, *items: Callable):
        for method in items:
            for typ in get_type_list(method):
                typ_list = self.registry.get(typ, set())
                typ_list.add(method)
                self.registry.update({typ: typ_list})

    def __contains__(self, item):
        pass


class Service:
    topic: str = ''

    def __init__(self):
        self.container = ServiceContainer()
        self.container.register(*get_methods(self))

        #
        message_types = list(self.container.registry.keys())
        self.message_type_adaptor = TypeAdapter(Union[tuple(message_types)])


def register(srvc: Service):
    def decorator(func):
        srvc.container.register(func)
        return func

    return decorator
