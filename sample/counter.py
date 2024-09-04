from shirdal import Application
from dataclasses import dataclass
from copy import copy


app = Application()


@dataclass
class PrintMessage:
    msg: str
    num: int
    endpoint: str = 'printer'


@app.service
def printer(msg: PrintMessage):
    print(msg.msg, msg.num)


for i in range(1, 1000):
    message = PrintMessage("hello world!", copy(i))  # if we do not copy the number all numbers would be common on 1000.
    # that's all we know
    app.operate(message)

input()  # we need this for program didn't get close before tasks gets done
