import pytest

__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


def test_basic():
    import tests.ordered_test
    assert tests.ordered_test.steps > 1
    assert tests.ordered_test.steps < 5

