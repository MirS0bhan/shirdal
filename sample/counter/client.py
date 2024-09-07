from shirdal import Application, Broker, BrokerType
from dataclasses import dataclass, asdict

broker = Broker.create(BrokerType.CLIENT, "localhost", 8282)

app = Application(broker)
broker.start()


@dataclass
class PrintMessage:
    msg: str
    num: int
    endpoint: str = 'printer'


message = asdict(PrintMessage("hello world!", 1))

app.operate(message)