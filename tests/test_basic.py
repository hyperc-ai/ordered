import pytest
import sys
sys.path.append("tests")

__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


def test_basic():
    # import tests.ordered_test
    import basic_ordered 
    assert basic_ordered.steps > 1
    assert basic_ordered.steps < 5


def test_basic_oo():
    # import tests.ordered_test
    import ordered_test
    assert ordered_test.steps > 1
    assert ordered_test.steps < 5

