from assertpy import assert_that

from interpolate import interpolate
import pytest


EPSILON = 1e-9


def test_interpolate_empty():
    with pytest.raises(ValueError):
        interpolate([])


def test_interpolate_repeated_x_values():
    with pytest.raises(ValueError):
        interpolate([(1, 2), (1, 3)])


def test_interpolate_degree_0():
    assert_that(interpolate([(1, 2)]).coefficients).is_equal_to([2])


def test_interpolate_degree_1():
    assert_that(interpolate([(1, 2), (2, 3)]).coefficients).is_equal_to([1, 1])


def test_interpolate_degree_3():
    points = [(1, 1), (2, 0), (-3, 2), (4, 4)]
    actual_polynomial = interpolate(points)
    expected_evaluations = points
    actual_evaluations = [(x, actual_polynomial.evaluateAt(x))
                          for (x, y) in expected_evaluations]

    for (p1, p2) in zip(expected_evaluations, actual_evaluations):
        for (a, b) in zip(p1, p2):
            assert_that(a).is_close_to(b, EPSILON)
