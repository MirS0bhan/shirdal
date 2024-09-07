from shirdal import Application
from dataclasses import dataclass
from time import sleep

app = Application()


@dataclass
class PrintMessage:
    msg: str
    endpoint: str = 'printer'


@app.service
def printer(msg: PrintMessage):
    print(msg.msg)


message = PrintMessage("hello world!")

app.operate(message)

sleep(0.000000000000001)  # we need this sleep to program didn't get colse before task run
