from assertpy import assert_that

from polynomial import strip
from polynomial import Polynomial


def test_strip_empty():
    assert_that(strip([], 1)).is_equal_to([])


def test_strip_single():
    assert_that(strip([1, 2, 3, 1], 1)).is_equal_to([1, 2, 3])


def test_strip_many():
    assert_that(strip([1, 2, 3, 1, 1, 1, 1], 1)).is_equal_to([1, 2, 3])


def test_strip_string():
    assert_that(strip("123111", "1")).is_equal_to("123")


def test_polynomial_zero():
    assert_that(Polynomial([0]).coefficients).is_equal_to([])
    assert_that(len(Polynomial([0]))).is_equal_to(0)


def test_polynomial_repr():
    f = Polynomial([1, 2, 3])
    assert_that(repr(f)).is_equal_to("1 + 2 x^1 + 3 x^2")


def test_polynomial_add():
    f = Polynomial([1, 2, 3])
    g = Polynomial([4, 5, 6])
    assert_that((f + g).coefficients).is_equal_to([5, 7, 9])


def test_polynomial_sub():
    f = Polynomial([1, 2, 3])
    g = Polynomial([4, 5, 6])
    assert_that((f - g).coefficients).is_equal_to([-3, -3, -3])


def test_polynomial_add_zero():
    f = Polynomial([1, 2, 3])
    g = Polynomial([0])
    assert_that((f + g).coefficients).is_equal_to([1, 2, 3])


def test_polynomial_negate():
    f = Polynomial([1, 2, 3])
    assert_that((-f).coefficients).is_equal_to([-1, -2, -3])


def test_polynomial_multiply():
    f = Polynomial([1, 2, 3])
    g = Polynomial([4, 5, 6])
    assert_that((f * g).coefficients).is_equal_to([4, 13, 28, 27, 18])


def test_polynomial_evaluate_at():
    f = Polynomial([1, 2, 3])
    assert_that((f(2))).is_equal_to(1 + 4 + 12)
