from shirdal import Application
from dataclasses import dataclass


app = Application()

@dataclass
class print_opr:
    data: str
    endpoint = 'printer'


@app.service
def printer(dt: print_opr):
    print(dt.data)

app.operate(print_opr(634165))
app.operate(print_opr(634165))
app.operate(print_opr(634165))
app.operate(print_opr(634165))

