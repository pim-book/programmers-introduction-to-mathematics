"""Euclidean geometry functions related to hyperbolic geometry."""

import math
from collections import namedtuple


EPSILON = 1e-8


def are_close(points1, points2):
    for p1, p2 in zip(sorted(points1), sorted(points2)):
        if (p1 - p2).norm() > EPSILON:
            return False
    return True


class Point(namedtuple('Point', ['x', 'y'])):
    """A point class which doubles as a vector class."""

    def norm(self):
        return math.sqrt(inner_product(self, self))

    def normalized(self):
        norm = self.norm()
        return Point(self.x / norm, self.y / norm)

    def project(self, w):
        """Project self onto the input vector w."""
        normalized_w = w.normalized()
        signedLength = inner_product(self, normalized_w)

        return Point(
            normalized_w.x * signedLength,
            normalized_w.y * signedLength)

    def __add__(self, other):
        x, y = other
        return Point(self.x + x, self.y + y)

    def __mul__(self, scalar):
        return Point(scalar * self.x, scalar * self.y)

    def __sub__(self, other):
        x, y = other
        return Point(self.x - x, self.y - y)

    def is_zero(self):
        return math.sqrt(inner_product(self, self)) < EPSILON

    def is_close_to(self, other):
        return (self - other).is_zero()

    def __str__(self):
        return 'Point(x={:.2f}, y={:.2f})'.format(self.x, self.y)

    def __repr__(self):
        return str(self)


def inner_product(v, w):
    return v.x * w.x + v.y * w.y


class Line:
    def __init__(self, point, slope):
        self.point = point
        self.slope = slope

    @staticmethod
    def through(p1, p2):
        """Return a Line through the two given points."""
        if abs(p1.x - p2.x) < EPSILON:
            return VerticalLine.at_point(p1)
        return Line(p1, (p2.y - p1.y) / (p2.x - p1.x))

    def intersect_with(self, line):
        """Compute the intersection of two lines.

        Raise an exception if they do not intersect in a single point.
        """
        if isinstance(line, VerticalLine):
            return line.intersect_with(self)

        if self == line:
            raise ValueError("Can't intersect two identical lines; "
                             "solution is not a single point.")

        if abs(self.slope) < EPSILON and abs(line.slope) < EPSILON:
            raise ValueError("Can't intersect two horizontal lines.")

        x1, y1, slope1 = self.point.x, self.point.y, self.slope
        x2, y2, slope2 = line.point.x, line.point.y, line.slope

        intersection_x = ((slope1 * x1 - slope2 * x2 + y2 - y1)
                          / (slope1 - slope2))
        intersection_y = y1 + slope1 * (intersection_x - x1)

        return Point(intersection_x, intersection_y)

    def y_value(self, x_value):
        """Compute the y value of the point on this line that has the given x
        value.
        """
        return self.slope * (x_value - self.point.x) + self.point.y

    def contains(self, point):
        x, y = point
        return abs(self.y_value(x) - y) < EPSILON

    def reflect(self, point):
        """Reflect a point across this line."""
        translated_to_origin = point - self.point
        projection = translated_to_origin.project(Point(1, self.slope))
        reflection_vector = translated_to_origin - projection
        return projection - reflection_vector + self.point

    def __eq__(self, other):
        if not isinstance(other, Line):
            return False

        if isinstance(other, VerticalLine):
            return other.__eq__(self)

        return (
            abs(self.slope - other.slope) < EPSILON
            and self.contains(other.point)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Line(point={}, slope={})".format(
            self.point, self.slope)

    def __repr__(self):
        return str(self)


class VerticalLine(Line):
    @staticmethod
    def at_point(point):
        """Return a VerticalLine instance based at the given point."""
        return VerticalLine(Point(point.x, 0), "vertical")

    def y_value(self, x_value):
        raise TypeError("VerticalLine does not support y_value")

    def reflect(self, point):
        """Reflect a point across this line."""
        return Point(2 * self.point.x - point.x, point.y)

    def intersect_with(self, line):
        """Compute the point of intersection of this vertical line with another
        line.

        Raise an exception if they do not intersect or if they are the same line.
        """
        if isinstance(line, VerticalLine):
            raise ValueError("Can't intersect two vertical lines; "
                             "solution is either empty or not a point.")

        return Point(self.point.x, line.y_value(self.point.x))

    def __eq__(self, other):
        return (
            isinstance(other, VerticalLine)
            and abs(self.point.x - other.point.x) < EPSILON
        )


class Circle(namedtuple('Circle', ['center', 'radius'])):
    def contains(self, point):
        """Compute whether a point is on a Euclidean circle."""
        center, radius = (self.center, self.radius)
        return abs(
            (point.x - center.x) ** 2
            + (point.y - center.y) ** 2
            - radius ** 2
        ) < EPSILON

    def tangent_at(self, point):
        """Compute the tangent line to a circle at a point.

        Raise an ValueError if the point is not on the circle.
        """
        if not self.contains(point):
            raise ValueError("Point is not on circle")

        if abs(point.y - self.center.y) < EPSILON:
            return VerticalLine.at_point(point)

        slope = -(point.x - self.center.x) / (point.y - self.center.y)
        return Line(point, slope)

    def invert_point(self, point):
        """Compute the inverse of a point with respect to a self.

        Raises a ValueError if the point to be inverted is the center
        of the circle.
        """
        x, y = point
        center, radius = (self.center, self.radius)
        square_norm = (x - center.x) ** 2 + (y - center.y) ** 2

        if math.sqrt(square_norm) < EPSILON:
            raise ValueError(
                "Can't invert the center of a circle in that same circle.")

        x_inverted = center.x + radius ** 2 * (x - center.x) / square_norm
        y_inverted = center.y + radius ** 2 * (y - center.y) / square_norm
        return Point(x_inverted, y_inverted)

    def intersect_with_line(self, line):
        """Return a possibly empty set containing the points of intersection
        of the context circle and the given line.
        """
        m = line.slope
        x, y = line.point.x, line.point.y
        c_x, c_y, r = self.center.x, self.center.y, self.radius
        if isinstance(line, VerticalLine):
            discriminant = r ** 2 - (x - c_x)**2
            if abs(discriminant) < EPSILON:
                discriminant = 0

            if discriminant < 0:
                return set()

            sqrt_disc = math.sqrt(discriminant)
            return set([
                Point(x, c_y + sqrt_disc),
                Point(x, c_y - sqrt_disc),
            ])
        else:
            A = m ** 2 + 1
            B = 2 * (m * y - m * c_y - c_x - m ** 2 * x)
            C = (
                c_x ** 2 + (m * x) ** 2 + (y - c_y) ** 2
                - 2 * m * x * y + 2 * m * x * c_y - r ** 2
            )
            discriminant = B * B - 4 * A * C
            if abs(discriminant) < EPSILON:
                discriminant = 0

            if discriminant < 0:
                return set()

            sqrt_disc = math.sqrt(discriminant)
            x_values = set([
                (-B + sqrt_disc) / (2 * A),
                (-B - sqrt_disc) / (2 * A),
            ])
            return set(
                Point(x, line.y_value(x)) for x in x_values
            )


def distance(p1, p2):
    """Compute the usual Euclidean plane distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] + p2[1]) ** 2)


def det3(A):
    """Compute the determinant of a 3x3 matrix"""
    if not (len(A) == 3 and len(A[0]) == 3):
        raise ValueError("Bad matrix dims")

    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def remove_column(A, removed_col_index):
    return [
        [entry for j, entry in enumerate(row) if j != removed_col_index]
        for row in A
    ]


def orientation(a, b, c):
    """Compute the orientation of three points visited in sequence, either
    'clockwise', 'counterclockwise', or 'collinear'.
    """
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = c
    value = (b_x - a_x) * (c_y - a_y) - (c_x - a_x) * (b_y - a_y)

    if (value > EPSILON):
        return 'counterclockwise'
    elif (value < -EPSILON):
        return 'clockwise'
    else:
        return 'collinear'


def circle_through_points_perpendicular_to_circle(point1, point2, circle):
    """Return a Circle that passes through the two given points and
    intersects the given circle at a perpendicular angle.

    A hyperbolic line between two points is computed as the circle arc
    perpendicular to the boundary circle that passes between those points.
    This can be constructed by first inverting one of the points in the
    circle, then constructing the circle passing through all three points.

    There are two cases when this may fail:

    (1) If the two points and the center of the input circle lie on a common
    line, then the hyperbolic line is a diameter of the circle. This function
    raises a ValueError in this case.

    (2) If the input points lie on the circle, then the inversion is a no-op.
    In this case we can compute the center of the desired circle as the point
    of intersection of the two tangent lines of the points.
    """
    if circle.contains(point1):
        if circle.contains(point2):
            circle_center = intersection_of_common_tangents(
                circle, point1, point2)
            radius = distance(circle_center, point1)
            return Circle(circle_center, radius)

        point3 = circle.invert_point(point2)
    else:
        point3 = circle.invert_point(point1)

    def row(point):
        (x, y) = point
        return [x ** 2 + y ** 2, x, y, 1]

    """The equation for the center of the circle passing through three points
    is given by the ratios of determinants of a cleverly chosen matrix. This
    corresponds to solving a system of three equations and three unknowns of
    the following form, where the unknowns are x0, y0, and r and the values x,
    y are set to the three points we wish the circle to pass through.

        (x - x0)^2 + (y - y0)^2 = r^2
    """
    M = [
        row(point1),
        row(point2),
        row(point3),
    ]

    detminor_1_1 = det3(remove_column(M, 0))
    if orientation(circle.center, point1, point2) == "collinear":
        raise ValueError("input points {} {} lie on a line with the "
                         "center of the circle {}".format(point1, point2, circle))

    # detminor stands for "determinant of (matrix) minor"
    detminor_1_2 = det3(remove_column(M, 1))
    detminor_1_3 = det3(remove_column(M, 2))
    detminor_1_4 = det3(remove_column(M, 3))

    circle_center_x = 0.5 * detminor_1_2 / detminor_1_1
    circle_center_y = -0.5 * detminor_1_3 / detminor_1_1
    circle_radius = (
        circle_center_x ** 2
        + circle_center_y ** 2
        + detminor_1_4 / detminor_1_1
    ) ** 0.5

    return Circle(Point(circle_center_x, circle_center_y), circle_radius)


def rotate_around_origin(angle, point):
    """Rotate the given point about the origin by the given angle (in radians).
    For the disk model, this is the same operation in Euclidean space: the
    application of a 2x2 rotation matrix.
    """
    rotation_matrix = [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)],
    ]

    x, y = point
    return Point(
        rotation_matrix[0][0] * x + rotation_matrix[0][1] * y,
        rotation_matrix[1][0] * x + rotation_matrix[1][1] * y,
    )


def intersection_of_common_tangents(circle, point1, point2):
    line1 = circle.tangent_at(point1)
    line2 = circle.tangent_at(point2)
    return line1.intersect_with(line2)


def bounding_box_area(points):
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)

    return (max_y - min_y) * (max_x - min_x)
