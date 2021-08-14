import pytest
import sys
sys.path.append("tests")

__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


def test_basic():
    # import tests.ordered_test
    import example_oo 
    assert example_oo.m.steps > 1
    assert example_oo.m.steps < 5

