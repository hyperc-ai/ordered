import random 

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

while x != 22:  
    random.choice([plus_x, minus_x])()  

print("Steps:", steps)

