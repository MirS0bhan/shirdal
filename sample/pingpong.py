import asyncio
from time import sleep

from shirdal import Service, MessagingSystem, Message


class Ping(Message):
    ni: int


class Pong(Message):
    no: int


class PingPong(Service):
    async def ping(self, message: Ping):
        print('ping', message)

        return Pong(no=message.ni + 1)

    async def pong(self, message: Pong):
        print('pong', message)

        return Ping(ni=message.no + 1)


ms = MessagingSystem('localhost', 6985, PingPong())
ms.start()

sleep(1)


async def main():
    await ms.publish(Ping(ni=5))


asyncio.run(main())
