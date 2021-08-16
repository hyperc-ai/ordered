__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


import ordered
import pytest


def frame_end():
    x = 1
    with ordered.orderedcontext():
        while x != 1:
            ordered.choice()()


def frame_end_good():
    x = 1
    with ordered.orderedcontext():
        while x != 1:
            ordered.choice()()
    pass  # required due to current Python limitation


def test_endofframe():
    "If ordered context's frame abruptly ends with nothing - pass statement is required"
    with pytest.raises(RuntimeError):
        frame_end()

def test_endofframe_fixed():
    frame_end_good()
