from shirdal import Application, Broker, BrokerType
from dataclasses import dataclass


broker = Broker.create(BrokerType.SERVER, "*", 8282)
app = Application(broker)
broker.start()


@dataclass
class PrintMessage:
    msg: str
    num: int
    endpoint: str = 'printer'


@app.service
def printer(msg):
    print(msg["msg"], msg["num"])

