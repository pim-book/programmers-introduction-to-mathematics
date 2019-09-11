from itertools import takewhile
from assertpy import assert_that

from newton import newton_sequence

EPSILON = 1e-4


def test_newtons_sequence_converge():
    def f(x):
        return x**5 - x - 1

    def f_derivative(x):
        return 5 * x**4 - 1

    starting_x = 1

    approximation = [
        (x, f(x))
        for x in list(newton_sequence(f, f_derivative, starting_x))
    ]

    assert_that(approximation[-1][0]).is_close_to(1.1673, EPSILON)
    assert_that(approximation[-1][1]).is_close_to(0, EPSILON)


def test_newtons_sequence_fails_to_converge():
    def f(x):
        return x**5 - x - 1

    def f_derivative(x):
        return 5 * x**4 - 1

    starting_x = 0
    approximation = [
        (x, f(x)) for (i, x) in takewhile(
            lambda z: z[0] < 10000,
            enumerate(newton_sequence(f, f_derivative, starting_x))
        )
    ]

    for (x, y) in approximation:
        assert_that(abs(x - 1.1673)).is_greater_than(EPSILON)
        assert_that(abs(y)).is_greater_than(EPSILON)


def test_newtons_sequence_converges_large_root():
    def f(x):
        return (x - 100)**5 - (x - 100) - 1

    def f_derivative(x):
        return 5 * (x - 100)**4 - 1

    starting_x = 103

    approximation = [
        (x, f(x))
        for x in list(newton_sequence(f, f_derivative, starting_x))
    ]

    assert_that(approximation[-1][0]).is_close_to(101.1673, EPSILON)
    assert_that(approximation[-1][1]).is_close_to(0, EPSILON)
