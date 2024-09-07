from shirdal import Application, Broker, BrokerType
from dataclasses import dataclass, asdict

broker = Broker.create(BrokerType.LOCAL)
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


message = asdict(PrintMessage("hello world!", 1))

app.operate(message)