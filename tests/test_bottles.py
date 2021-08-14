import sys
sys.path.append("tests")

__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


def test_bottle_definition():
    import example_bottle_manual
    assert example_bottle_manual.b2.fill == 4


def test_bottle_solve():
    import example_bottle
    assert example_bottle.b2.fill == 4


