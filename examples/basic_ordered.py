# TODO: create an OO version
import sys
sys.path.append(".")

import random, ordered

x = 5
steps = 0

def plus_x():
    global x, steps
    x += 7
    steps += 1

def minus_x():
    global x, steps
    x -= 2
    steps += 1

with ordered.orderedcontext(): 
    # exit ordered context with minimum steps, no exceptions
    while x != 22:  
        random.choice([plus_x, minus_x])()  

print("Steps:", steps)

