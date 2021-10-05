from assertpy import assert_that
import math
import pytest

from geometry import *
from testing import *


def test_are_close():
    pts1 = [Point(1.0, 2.0), Point(3.0, 3.999999999999999999)]
    pts2 = [Point(0.99999999999999, 2.0), Point(3.0, 4.0)]
    assert_that(are_close(pts1, pts2)).is_true()


def test_are_close_false():
    pts1 = [Point(1.0, 2.0), Point(3.0, 4.0)]
    pts2 = [Point(0.9, 2.0), Point(3.0, 4.0)]
    assert_that(are_close(pts1, pts2)).is_false()


def test_bounding_box_area():
    pts = [Point(1.0, 2.0), Point(3.0, 4.0), Point(5.0, 6.0)]
    assert_that(bounding_box_area(pts)).is_equal_to(4.0 * 4.0)


def test_line_y_value():
    line = Line(Point(2, 3), slope=4)
    assert_that(line.y_value(x_value=4)).is_equal_to(11)


def test_vertical_line_y_value():
    line = VerticalLine.at_point(Point(2, 3))
    with pytest.raises(TypeError):
        line.y_value(x_value=4)


def test_line_eq():
    line1 = Line(Point(1, 0), slope=2)
    line2 = Line(Point(2, 2), slope=2)
    assert_that(line1).is_equal_to(line2)
    assert_that(line2).is_equal_to(line1)


def test_line_neq():
    line1 = Line(Point(1, 0), slope=2)
    line2 = Line(Point(0, -2), slope=2.1)
    assert_that(line1 != line2).is_true()
    assert_that(line2 != line1).is_true()
    assert_that(line2 != 7).is_true()
    assert_that(line2 != 7).is_true()


def test_vertical_line_eq():
    line1 = VerticalLine.at_point(Point(2, 5))
    line2 = VerticalLine.at_point(Point(2, -1))
    assert_that(line1 == line2).is_true()
    assert_that(line2 == line1).is_true()


def test_vertical_line_neq():
    line1 = VerticalLine.at_point(Point(2, 5))
    line2 = VerticalLine.at_point(Point(2.1, -1))
    assert_that(line1 != line2).is_true()
    assert_that(line2 != line1).is_true()


def test_vertical_line_neq_line():
    line1 = VerticalLine.at_point(Point(2, 5))
    line2 = Line(Point(2, 5), slope=1)
    assert_that(line1 != line2).is_true()
    assert_that(line2.__ne__(line1)).is_true()


def test_vertical_line_str():
    line = Line(Point(2, 5), slope=1)
    assert_that(str(line)).is_equal_to(
        "Line(point={}, slope=1)".format(line.point))
    assert_that(repr(line)).is_equal_to(str(line))


def test_line_intersect_with():
    line1 = Line(Point(4, 3), slope=2)
    line2 = Line(Point(-2, -1), slope=1)
    assert_that(line1.intersect_with(line2)).is_equal_to(Point(6, 7))
    assert_that(line2.intersect_with(line1)).is_equal_to(Point(6, 7))


def test_line_intersect_with_both_horizontal():
    line1 = Line(Point(4, 3), slope=0)
    line2 = Line(Point(-2, -1), slope=0)
    with pytest.raises(ValueError):
        line1.intersect_with(line2)


def test_line_intersect_with_self():
    line1 = Line(Point(4, 3), slope=0)
    with pytest.raises(ValueError):
        line1.intersect_with(line1)


def test_vertical_line_intersect_with():
    line1 = VerticalLine.at_point(Point(4, -10))
    line2 = Line(Point(-2, -1), slope=1)
    assert_that(line1.intersect_with(line2)).is_equal_to(Point(4, 5))
    assert_that(line2.intersect_with(line1)).is_equal_to(Point(4, 5))


def test_vertical_line_intersect_with_vertical_line():
    line1 = VerticalLine.at_point(Point(4, -10))
    line2 = VerticalLine.at_point(Point(5, 2))
    with pytest.raises(ValueError):
        line1.intersect_with(line2)


def test_vertical_line_intersect_with_self():
    line1 = Line(Point(4, 3), slope=0)
    with pytest.raises(ValueError):
        line1.intersect_with(line1)


def test_circle_contains():
    circle = Circle(center=Point(0, 0), radius=1)
    points = [
        Point(1, 0),
        Point(0, 1),
        Point(math.cos(2 * math.pi / 5), math.sin(2 * math.pi / 5)),
    ]
    for point in points:
        assert_that(circle.contains(point)).is_true()


def test_tangent_at_point_not_on_circle():
    circle = Circle(center=Point(0, 0), radius=1)
    point = Point(0, 2)
    with pytest.raises(ValueError):
        circle.tangent_at(point)


def test_tangent_at_produces_vertical_line():
    circle = Circle(center=Point(0, 0), radius=1)
    point = Point(1, 0)
    expected_line = VerticalLine.at_point(point)
    assert_that(circle.tangent_at(point)).is_equal_to(expected_line)


def test_tangent_at_simple():
    circle = Circle(center=Point(0, 0), radius=1)
    point = Point(0, 1)
    expected_line = Line(point=point, slope=0)
    assert_that(circle.tangent_at(point)).is_equal_to(expected_line)


def test_tangent_at_angled():
    circle = Circle(center=Point(1, 2), radius=2)
    sqrt3 = math.sqrt(3)
    point = Point(2, 2 + sqrt3)
    expected_line = Line(point=point, slope=-1/sqrt3)
    assert_that(circle.tangent_at(point)).is_equal_to(expected_line)


def test_invert_in_circle_horizontal():
    circle = Circle(center=Point(1, 1), radius=5)
    point = Point(4, 1)
    expected_inverse = Point(1 + 25 / 3, 1)
    assert_that(circle.invert_point(point)).is_equal_to(expected_inverse)


def test_invert_in_circle_diagonal():
    circle = Circle(center=Point(0, 0), radius=2 ** 0.5)
    point = Point(2, 2)
    expected_inverse = Point(1/2, 1/2)
    actual_inverse = circle.invert_point(point)
    assert_are_close(actual_inverse, expected_inverse)


def test_invert_in_circle_center():
    circle = Circle(center=Point(1, 2), radius=2 ** 0.5)
    point = Point(1, 2)
    with pytest.raises(ValueError):
        circle.invert_point(point)


def test_circle_through_points_unit_circle():
    reference_circle = Circle(Point(0, 0), 1)
    p1 = Point(1/2, 1/2)
    p2 = Point(1/2, -1/2)

    expected_circle = Circle(Point(3/2, 0), (5/4) ** 0.5)
    actual_circle = circle_through_points_perpendicular_to_circle(
        p1, p2, reference_circle)
    assert_that(expected_circle).is_equal_to(actual_circle)


def test_circle_through_points_diameter():
    reference_circle = Circle(Point(0, 0), 1)
    p1 = Point(1/3, 1/4)
    p2 = Point(-1/3, -1/4)

    with pytest.raises(ValueError):
        circle_through_points_perpendicular_to_circle(p1, p2, reference_circle)


def test_rotate_around_origin_pi_over_3():
    angle = math.pi / 3
    assert_are_close(Point(1 / 2, 3 ** 0.5 / 2),
                     rotate_around_origin(angle, (1, 0)))
    assert_are_close(Point(-3 ** 0.5 / 2, 1/2),
                     rotate_around_origin(angle, (0, 1)))


def test_circle_through_points_with_points_on_circle():
    reference_circle = Circle(Point(0, 0), radius=1)
    n = 6
    z = math.cos(math.pi / 6) ** 2 / math.sin(math.pi / 6)
    y1 = -1 / z
    y2 = 1 / z
    x = math.sqrt(1 - y1**2)

    p1 = Point(x, y1)
    p2 = Point(x, y2)

    expected_circle = Circle(center=Point(
        x=1.3416407864998734, y=0), radius=0.8944271909999155)
    actual_circle = circle_through_points_perpendicular_to_circle(
        p1, p2, reference_circle)
    assert_are_close(expected_circle.center, actual_circle.center)
    assert_are_close(expected_circle.radius, actual_circle.radius)


def test_circle_through_points_with_one_point_on_circle():
    reference_circle = Circle(Point(0, 0), 1)
    p1 = Point(1/2, 1/2)
    p2 = Point(2/3, - math.sqrt(5) / 3)

    expected_circle = Circle(Point(3/2, 0), (5/4) ** 0.5)
    actual_circle = circle_through_points_perpendicular_to_circle(
        p1, p2, reference_circle)
    assert_are_close(expected_circle.center, actual_circle.center)
    assert_are_close(expected_circle.radius, actual_circle.radius)
    actual_circle = circle_through_points_perpendicular_to_circle(
        p2, p1, reference_circle)
    assert_are_close(expected_circle.center, actual_circle.center)
    assert_are_close(expected_circle.radius, actual_circle.radius)


def test_reflect_increasing_slope():
    line = Line(Point(0, 0), 1)
    assert_are_close(line.reflect(Point(2, -2)), Point(-2, 2))
    assert_are_close(line.reflect(Point(-6, 4)), Point(4, -6))
    assert_are_close(line.reflect(Point(4, 4)), Point(4, 4))


def test_reflect_decreasing_slope():
    line = Line(Point(-1, -2), -1)
    assert_are_close(line.reflect(Point(-2, -3)), Point(0, -1))


def test_circle_intersect_with_vertical_line():
    line = VerticalLine.at_point(Point(math.cos(math.pi / 4), -1))
    circle = Circle(Point(0, 0), 1)
    assert_iterables_are_close(
        circle.intersect_with_line(line),
        set([
            Point(math.cos(math.pi / 4), math.sin(math.pi / 4)),
            Point(math.cos(math.pi / 4), -math.sin(math.pi / 4))
        ]))


def test_circle_intersect_with_vertical_tangent():
    line = VerticalLine.at_point(Point(-1, -1))
    circle = Circle(Point(0, 0), 1)
    assert_iterables_are_close(
        circle.intersect_with_line(line),
        set([Point(-1, 0)]))


def test_circle_intersect_with_vertical_line_empty():
    line = VerticalLine.at_point(Point(-2, -1))
    circle = Circle(Point(0, 0), 1)
    assert_that(circle.intersect_with_line(line)).is_empty()


def test_circle_intersect_with_line():
    line = Line(Point(-1, -1), 1)
    circle = Circle(Point(0, 0), 1)
    assert_iterables_are_close(
        circle.intersect_with_line(line),
        set([
            Point(math.cos(math.pi / 4), math.sin(math.pi / 4)),
            Point(-math.cos(math.pi / 4), -math.sin(math.pi / 4))
        ]))


def test_circle_intersect_with_line_tangent():
    tangency_point = Point(math.cos(math.pi / 4), math.sin(math.pi / 4))
    line = Line(tangency_point + Point(-3, 3), -1)
    circle = Circle(Point(0, 0), 1)
    assert_iterables_are_close(
        circle.intersect_with_line(line),
        set([tangency_point]))


def test_circle_intersect_with_line_empty():
    tangency_point = Point(math.cos(math.pi / 4), math.sin(math.pi / 4))
    line = Line(tangency_point + Point(-3, 7), -2)
    circle = Circle(Point(0, 0), 1)
    assert_that(circle.intersect_with_line(line)).is_empty()


def test_orientation_counterclockwise():
    p1 = Point(1, 1)
    p2 = Point(2, 2)
    p3 = Point(1.5, 3)
    assert_that(orientation(p1, p2, p3)).is_equal_to("counterclockwise")
    assert_that(orientation(p1, p2, p3)).is_equal_to("counterclockwise")


def test_orientation_clockwise():
    p1 = Point(1, 1)
    p2 = Point(2, 2)
    p3 = Point(3, 1.5)
    assert_that(orientation(p1, p2, p3)).is_equal_to("clockwise")


def test_orientation_collinear():
    p1 = Point(1, 2)
    p2 = Point(2, 4)
    p3 = Point(3, 6)
    assert_that(orientation(p1, p2, p3)).is_equal_to("collinear")


def test_det3_error():
    with pytest.raises(ValueError):
        det3([])
