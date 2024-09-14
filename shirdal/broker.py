import asyncio
from threading import Thread
from typing import (
    AsyncGenerator,
    Callable,
    Coroutine,
    Optional,
    Any,

    Dict,
)

import zmq
import msgpack

from shirdal import Service, Message


def serialize_message(message: Dict[str, Any]) -> bytes:
    """Serialize a message dictionary into bytes using msgpack."""
    return msgpack.packb(message)


def deserialize_message(raw_message: bytes) -> Dict[str, Any]:
    """Deserialize raw bytes into a message dictionary using msgpack."""
    return msgpack.unpackb(raw_message)


async def publisher(
        context: zmq.Context,
        host: str, port: int, topic: str,
        serializer: Callable[[Dict[str, Any]], bytes]
        ) -> Callable[[Message], Coroutine[Any, None, None]]:

    socket: zmq.Socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://{host}:{port}")
    topic_encoded: bytes = topic.encode('utf-8') + b'\0'

    async def publish(message: Message) -> None:
        raw_bin_msg: bytes = serializer(message.model_dump())
        socket.send(raw_bin_msg)

    return publish


async def subscribe(
        context: zmq.Context, host: str, port: int, topic: str
) -> AsyncGenerator[Dict[str, Any], None]:
    socket: zmq.Socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{host}:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    while True:
        raw_bin_msg: bytes = socket.recv()
        # Split the topic from the message
        raw_msg = raw_bin_msg
        message_dict: Dict[str, Any] = deserialize_message(raw_msg)
        yield message_dict


async def executor(
        subscriber: AsyncGenerator[Dict[str, Any], None],
        publish: Callable[[Message], Coroutine[Any, None, None]],
        service: Service
) -> None:
    async for message in subscriber:
        validated_message: Message = service.message_type_adaptor.validate_python(message)
        async for func in service.container.resolve(validated_message):
            r = await func(validated_message)
            if r:
                await publish(r)


class MessagingSystem(Thread):
    def __init__(self, host: str, port: int, service: Service):
        super().__init__()
        self.host: str = host
        self.port: int = port

        self.service: Service = service
        self.topic: str = service.topic
        self.context: zmq.Context = zmq.Context()

        self.publish: Optional[Callable[[Message], Coroutine[None, None, None]]] = None
        self.subscriber: Optional[AsyncGenerator[Dict, None]] = None

    async def _run(self) -> None:
        # Launch publisher and subscriber
        self.publish = await publisher(self.context, self.host, self.port, self.topic, serialize_message)
        self.subscriber = subscribe(self.context, self.host, self.port, self.topic)
        # Run the executor to process incoming messages
        await executor(self.subscriber, self.publish, self.service)

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._run())
        finally:
            loop.close()
