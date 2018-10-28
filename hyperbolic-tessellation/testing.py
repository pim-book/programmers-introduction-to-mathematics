from assertpy import fail
from geometry import EPSILON


def is_close(v1, v2):
    try:
        return v1.is_close_to(v2)
    except AttributeError:
        return abs(v1 - v2) < EPSILON


def assert_are_close(v1, v2):
    if not is_close(v1, v2):
        fail("Expected {} to to be close to {}, but it wasn't".format(
            v1, v2))


def assert_iterables_are_close(s1, s2):
    for item1, item2 in zip(s1, s2):
        assert_are_close(item1, item2)
