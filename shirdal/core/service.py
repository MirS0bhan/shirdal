from typing import Callable

from shirdal.utils import get_methods, get_type_list

from container import ContainerAbstract


class ServiceContainer(ContainerAbstract):
    def __init__(self):
        self.registry = {}

    def resolve(self, name: str):
        pass

    def register(self, *items: Callable):
        for method in items:
            for typ in get_type_list(method):
                typ_list = self.registry.get(typ, set())
                typ_list.add(method)
                self.registry.update({typ: typ_list})

    def __contains__(self, item):
        pass


class Service:
    def __init__(self):
        self.container = ServiceContainer()
        self.container.register(*get_methods(self))


def register(srvc: Service):
    def decorator(func):
        srvc.container.register(func)
        return func

    return decorator
