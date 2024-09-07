from shirdal import Application, Broker, BrokerType
from dataclasses import dataclass

import cProfile


broker = Broker.create(BrokerType.SERVER, "*", 8282)

app = Application(broker)


@dataclass
class PrintMessage:
    msg: str
    num: int
    endpoint: str = 'printer'


@app.service
def printer(msg: PrintMessage):
    print(msg["msg"], msg["num"])


cProfile.run("broker.start()")
