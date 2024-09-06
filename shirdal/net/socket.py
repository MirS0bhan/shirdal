from abc import ABC, abstractmethod

import zmq

from .serialize import Serializer


class SocketAbstract(ABC):
    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def recv(self):
        pass

    @abstractmethod
    def setup(self):
        pass


class Socket(SocketAbstract, ABC):
    _ROLE = None

    def __init__(self, serializer: Serializer):
        self.context = zmq.Context()
        self.socket = self.context.socket(self._ROLE)
        self.serializer = serializer

    def send(self, message):
        serialized_message = self.serializer.serialize(message)
        self.socket.send(serialized_message)

    def recv(self):
        serialized_response = self.socket.recv()
        return self.serializer.deserialize(serialized_response)


class ServerSocket(Socket):
    _ROLE = zmq.REP

    def __init__(self, serializer: Serializer, port: int = 6985):
        super().__init__(serializer)
        self.port = port
        self.socket = self.context.socket(self._ROLE)

    def setup(self):
        self.socket.bind(f'tcp://*:{self.port}')
        print(f"Server is running and listening on port {self.port}...")


class ClientSocket(Socket):
    _ROLE = zmq.REQ

    def __init__(self, serializer: Serializer, host: str = 'localhost', port: int = 6985):
        super().__init__(serializer)
        self.host = host
        self.port = port
        self.socket = self.context.socket(self._ROLE)

    def setup(self):
        self.socket.connect(f'tcp://{self.host}:{self.port}')
