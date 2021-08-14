import pytest, gc
import ordered, random

__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


class MyVars:
    x: int
    steps: int
    def __init__(self) -> None:
        self.x = 0
        self.steps = 0

    def plus_x(self):
        self.x += 3
        count_steps(self)

    def minus_x(self):
        self.x -= 2
        count_steps(self)
    
def count_steps(o: MyVars):
    o.steps += 1


# @pytest.mark.skip(reason="TODO")
def test_partial_context_oo_3():
    m = MyVars()
    m.x = 5
    with ordered.orderedcontext():
        # exit ordered context without exceptions with minimum steps
        while m.x != 12:  
            ordered.choice()()  
    assert m.x == 12
    assert m.steps == 4


