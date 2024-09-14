import asyncio
from time import ctime

from shirdal import MessagingSystem, Service, Message


class PrintMessage(Message):
    msg: str


class Log(Message):
    time: str
    message: str


class Printer(Service):
    async def printer(self, msg: PrintMessage):
        print(msg.msg)
        return Log(message=msg.msg, time=ctime())

    async def log(self, log: Log):
        print("message", log.message, "printed at:", log.time)


ms = MessagingSystem('localhost', 6985, Printer())
ms.start()


async def main():
    await asyncio.sleep(0.1)
    message = PrintMessage(msg="hello world!")

    await ms.publish(message)
    await asyncio.sleep(1)
    await ms.publish(message)


asyncio.run(main())
