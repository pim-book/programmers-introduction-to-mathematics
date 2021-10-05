from assertpy import assert_that
import numpy

from svd import svd

EPSILON = 1e-9


def test_reconstruct_matrix_from_svd():
    matrix = numpy.array([
        [2, 5, 3],
        [1, 2, 1],
        [4, 1, 1],
        [3, 5, 2],
        [5, 3, 1],
        [4, 5, 5],
        [2, 4, 2],
        [2, 2, 5],
    ], dtype='float64')

    singular_values, us, vs = svd(matrix)
    singular_value_matrix = numpy.diag(singular_values)

    reconstructed_matrix = numpy.dot(
        us, numpy.dot(singular_value_matrix, vs))

    flattened_original = matrix.flatten()
    flattened_actual = reconstructed_matrix.flatten()

    for (a, b) in zip(flattened_actual, flattened_original):
        assert_that(a).is_close_to(b, EPSILON)


def test_svd_of_transpose():
    matrix = numpy.array([
        [2, 5, 3],
        [1, 2, 1],
        [4, 1, 1],
        [3, 5, 2],
        [5, 3, 1],
        [4, 5, 5],
        [2, 4, 2],
        [2, 2, 5],
    ], dtype='float64').T

    singular_values, us, vs = svd(matrix)
    singular_value_matrix = numpy.diag(singular_values)

    reconstructed_matrix = numpy.dot(
        us, numpy.dot(singular_value_matrix, vs))

    flattened_original = matrix.flatten()
    flattened_actual = reconstructed_matrix.flatten()

    for (a, b) in zip(flattened_actual, flattened_original):
        assert_that(a).is_close_to(b, EPSILON)


def test_1_by_1():
    matrix = numpy.array([[2]], dtype='float64')
    singular_values, us, vs = svd(matrix)
    assert_that(singular_values).is_equal_to([2])
    assert_that(us).is_length(1)
    assert_that(vs).is_length(1)

    if us[0] == [-1.0]:
        assert_that(vs[0]).is_equal_to([-1.0])
    else:
        assert_that(us[0]).is_equal_to([1.0])
        assert_that(vs[0]).is_equal_to([1.0])
