import sys
sys.path.append(".")

import ordered
import gc

class MyVars:
    x: int
    def __init__(self) -> None:
        self.x = 0

m = MyVars()
m.x = 5
steps = 0

def plus_x(m: MyVars):
    m.x += 3
    global steps
    steps += 1

def minus_x(m: MyVars):
    m.x -= 2
    global steps
    steps += 1


with ordered.orderedcontext():
    # exit ordered context without exceptions with minimum steps
    while m.x != 12:  
        ordered.choice([plus_x, minus_x])(ordered.choice(gc.get_objects()))  
    # hello

print("Steps:", steps)

