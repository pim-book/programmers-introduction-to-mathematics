from assertpy import assert_that
from geometry import Point
from tessellation import TessellationConfiguration
import math

from hyperbolic import *
from testing import *


def test_fundamental_triangle():
    config = TessellationConfiguration(6, 4)
    center, pi_over_q_vertex, x_axis_vertex = compute_fundamental_triangle(
        config)
    assert_that(center).is_equal_to(Point(0, 0))
    assert_iterables_are_close(x_axis_vertex, Point(math.sqrt(2) - 1, 0))

    b_x = 0.5 * math.sqrt(6 - 3 * math.sqrt(3))
    b_y = 0.5 * math.sqrt(2 - math.sqrt(3))
    assert_iterables_are_close(pi_over_q_vertex, Point(x=b_x, y=b_y))


def test_poincare_disk_line_reflect():
    line = PoincareDiskLine(Point(0, 0), radius=2 ** 0.5)
    point = Point(2, 2)
    expected_inverse = Point(1/2, 1/2)
    actual_inverse = line.reflect(point)
    assert_are_close(actual_inverse, expected_inverse)


def test_poincare_disk_model_line_through_diameter():
    model = PoincareDiskModel(Point(0, 0), radius=1)
    p1 = Point(1/6, 1/5)
    p2 = Point(2/6, 2/5)
    actual_line = model.line_through(p1, p2)
    expected_line = Line(Point(1/6, 1/5), slope=6/5)
    assert_that(expected_line).is_equal_to(actual_line)


def test_poincare_disk_model_line_through_hyperbolic():
    model = PoincareDiskModel(Point(0, 0), radius=1)
    p1 = Point(1/2, 1/2)
    p2 = Point(1/2, -1/2)
    actual_line = model.line_through(p1, p2)
    expected_line = PoincareDiskLine(Point(3/2, 0), (5/4) ** 0.5)
    assert_that(expected_line).is_equal_to(actual_line)
