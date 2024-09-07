from typing import Dict, Union, Callable, Container as Ctrn

from shirdal.utils import get_name


class Container(Ctrn):
    def __init__(self):
        self.registry: Dict[str, Union[object, Callable]] = {}

    def register(self, *item: Union[object, Callable]):
        for i in item:
            item_name = get_name(i)
            self.registry[item_name] = i

    def resolve(self, name: str):
        return self.registry[name]

    def __contains__(self, item: str | Union[object, Callable]):
        if type(item) is str:
            return item in self.registry.keys()
        else:
            return item in self.registry.values()
