__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


import ordered
import pytest

x = 0
def inc():
    global x
    x += 1

def run_inc():
    global x
    with ordered.orderedcontext():
        while x != 1:
            ordered.choice()()
    pass  # required due to current Python limitation

@pytest.mark.skip("Fix requested at https://github.com/hyperc-ai/ordered/issues/2")
def test_global_access():
    "Setting the breakpoint to line 13 should work"
    run_inc()

