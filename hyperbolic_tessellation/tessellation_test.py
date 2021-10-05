from geometry import Point
from geometry import rotate_around_origin
import math
import pytest

from tessellation import *
from testing import *


def test_valid_configuration():
    TessellationConfiguration(6, 4)
    TessellationConfiguration(4, 5)
    TessellationConfiguration(7, 3)
    TessellationConfiguration(3, 7)


def test_invalid_configuration():
    with pytest.raises(ValueError):
        TessellationConfiguration(4, 4)


def test_center_polygon():
    config = TessellationConfiguration(6, 4)
    tessellation = HyperbolicTessellation(config)

    b_x = 0.5 * math.sqrt(6 - 3 * math.sqrt(3))
    b_y = 0.5 * math.sqrt(2 - math.sqrt(3))
    starting_vertex = Point(x=b_x, y=b_y)

    vertices = [
        rotate_around_origin(k * math.pi / 3, starting_vertex)
        for k in range(6)
    ]

    assert_iterables_are_close(tessellation.compute_center_polygon(), vertices)
