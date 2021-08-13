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


def test_partial_context_oo():
    m = MyVars()
    m.x = 5

    def plus_x(m: MyVars):
        m.x += 3
        m.steps += 1

    def minus_x(m: MyVars):
        m.x -= 2
        m.steps += 1

    with ordered.orderedcontext():
        # exit ordered context without exceptions with minimum steps
        while m.x != 12:  
            ordered.choice([plus_x, minus_x])(ordered.choice(gc.get_objects()))  
    assert m.x == 12
    assert m.steps == 4


