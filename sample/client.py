from shirdal import Application, Broker, BrokerType
from dataclasses import dataclass

import cProfile
import time
from timeit import timeit

broker = Broker.create(BrokerType.CLIENT,"localhost",8282)

app = Application(broker)
broker.start()

@dataclass
class PrintMessage:
    msg: str
    num: int
    endpoint: str = 'printer'


message = PrintMessage("hello world!", 1)


iterations = 100000
total_time = timeit("app.operate(message)", number=iterations, globals=globals())
print(total_time)
print(f"Average time is {total_time / iterations:.6f} seconds")

