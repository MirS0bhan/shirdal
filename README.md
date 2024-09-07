# shirdal

## philosophy
...

## advantages 
- simple, predefined, logicful 
- create softwares that is both localy and SAAS and also it is easy to move services 
- have a Publisher/Subscriber archtecture for microservice systems 
- create interfaces like CLI, AI so easy

## usage 
### installation
#### Pypi
```bash
pip install shirdal
```

#### github
```bash
gh repo clone MirS0bhan/shirdal && cd shirdal
pip install .
```

### get start
let's define a hello world printer 
```python
from shirdal import Application, Broker, BrokerType
from dataclasses import dataclass, asdict

broker = Broker.create(BrokerType.LOCAL)
app = Application(broker)
broker.start()

@dataclass
class PrintMessage:
    msg: str
    endpoint: str = 'printer'

    
@app.service
def printer(msg):
    print(msg["msg"])


message = asdict(PrintMessage("hello world!", 1))

app.operate(message)
```


