from shirdal.utils import get_methods

from container import Container


class Service:
    def __init__(self):
        self.__cnt = Container()
        self.__cnt.register(*get_methods(self))
