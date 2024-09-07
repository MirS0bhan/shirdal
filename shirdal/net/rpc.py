from typing import Type, Dict, Any, List

from .socket import ServerSocket, ClientSocket
from .serialize import MsgPackSerializer, Serializer

from pydantic import BaseModel


class Params(BaseModel):
    args: List[Any] = []
    kwargs: Dict[Any, Any] = {}


class Message(BaseModel):
    method: str
    params: Params


class ServerRPC(ServerSocket):
    def __init__(self, port, serializer: Type[Serializer] = MsgPackSerializer):
        super().__init__(serializer(), port)

    def _start_server(self):
        self.setup()

        while True:
            raw = self.recv()
            message = Message(**raw)
            response = self._process_request(message)
            self.send(response)

    def _process_request(self, request: Message):
        func = getattr(self, request.method, None)

        if callable(func):
            return func(*request.params.args, **request.params.kwargs)

        return {'error': 'Unknown method'}


class ClientRPC(ClientSocket):
    def __init__(self, host, port):
        serializer = MsgPackSerializer()
        super().__init__(serializer, host, port)
        self.setup()

    def _call(self, method, *args, **kwargs):
        request = Message(
            method=method,
            params=Params(
                args=args,
                kwargs=kwargs
            )
        ).model_dump()

        self.send(request)
        response = self.recv()
        return response
