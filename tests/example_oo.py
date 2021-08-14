import ordered

class MyVars:
    x: int
    steps: int
    def __init__(self) -> None:
        self.x = 0
        self.steps = 0

    def plus_x(self):
        self.x += 3
        self.count_steps()

    def minus_x(self):
        self.x -= 2
        self.count_steps()
    
    def count_steps(self):
        self.steps += 1

m = MyVars()
m.x = 5
with ordered.orderedcontext():
    # exit ordered context without exceptions with minimum steps
    while m.x != 12:  
        ordered.choice()()  

print("Steps:", m.steps)