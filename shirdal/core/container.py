from typing import Dict, Union, Callable, Container as CTNR


def get_name(item: Union[object, Callable]) -> str:
    match item.__class__.__name__:
        case 'type' | 'function':
            return item.__name__
        case _:
            return item.__class__.__name__


class Container(CTNR):
    def __init__(self):
        self.registry: Dict[str, Union[object, Callable]] = {}

    def register(self, item: Union[object, Callable]):
        item_name = get_name(item)
        self.registry[item_name] = item

    def resolve(self, name: str):
        return self.registry[name]

    def __contains__(self, item: str | Union[object, Callable]):
        if type(item) is str:
            return item in self.registry.keys()
        else:
            return item in self.registry.values()
