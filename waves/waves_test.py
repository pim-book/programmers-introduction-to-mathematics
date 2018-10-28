from assertpy import assert_that
import numpy
import pytest

from waves import bead_matrix
from waves import sorted_eigensystem
from waves import decompose

EPSILON = 1e-5


def normalize(v):
    norm = numpy.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def test_bead_matrix_fail():
    with pytest.raises(ValueError):
        bead_matrix(dimension=3)


def test_bead_matrix():
    expected_matrix = numpy.array(
        [
            [-2, 1, 0, 0, 0],
            [1, -2, 1, 0, 0],
            [0, 1, -2, 1, 0],
            [0, 0, 1, -2, 1],
            [0, 0, 0, 1, -2],
        ]
    )

    flattened_expected = expected_matrix.flatten()
    flattened_actual = bead_matrix(dimension=5).flatten()
    for (a, b) in zip(flattened_actual, flattened_expected):
        assert_that(a).is_close_to(b, EPSILON)


def test_sorted_eigensystem():
    matrix = numpy.array(
        [
            [1, 1, 2],
            [-1, 3, 2],
            [-1, 2, 3],
        ]
    )

    eigenvalues, eigenvectors = sorted_eigensystem(matrix)
    expected_eigenvalues = [4, 2, 1]
    expected_eigenvectors = numpy.array([
        numpy.array([1, 1, 1]) / numpy.sqrt(3),
        numpy.array([-3, -1, -1]) / numpy.sqrt(11),
        numpy.array([-2, -2, 1]) / 3,
    ])

    for (e1, e2) in zip(eigenvalues, expected_eigenvalues):
        assert_that(e1).is_close_to(e2, EPSILON)

    for (v1, v2) in zip(eigenvectors, expected_eigenvectors):
        for (a, b) in zip(v1, v2):
            assert_that(a).is_close_to(b, EPSILON)


def test_decompose():
    eigenvectors = numpy.array(
        [
            numpy.array([1, 1, 1]) / numpy.sqrt(3),
            numpy.array([-3, -1, -1]) / numpy.sqrt(11),
            numpy.array([-2, -2, 1]) / 3,
        ]
    )

    vector = numpy.array([1, 2, 3])
    decomposition = decompose(eigenvectors, vector)

    expected_decomposition = {
        0: (1 + 2 + 3) / 3**0.5,
        1: (-3 - 2 - 3) / 11**0.5,
        2: (-2 - 4 + 3) / 3,
    }

    for key in decomposition.keys():
        assert_that(decomposition[key]).is_close_to(
            expected_decomposition[key], EPSILON)
