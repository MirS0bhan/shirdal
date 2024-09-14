import asyncio
from profile import run


from shirdal import MessagingSystem, Service, Message


class PrintMessage(Message):
    message: str


class Printer(Service):
    async def printer(self, msg: PrintMessage):
        pass


ms = MessagingSystem('localhost', 6985, Printer())
ms.start()


async def main():
    await asyncio.sleep(0.1)
    message = PrintMessage(message="hello world!")

    for _ in range(10000):
        await ms.publish(message)



run('asyncio.run(main())',sort=1)
