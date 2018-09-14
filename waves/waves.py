from collections import deque

import numpy


def shift(array, shift_amount):
    """Shift a list right (positive) or left (negative) by a given amount,
    filling new entries with zero.

    Arguments:
        array: the array to shift
        shift_amount: an integer number of places to shift.

    Returns:
        A shifted array, with new entries being zero.

    >>> shift([1, -2, 1, 0, 0], 1)
    [0, 1, -2, 1, 0]
    >>> shift([1, -2, 1, 0, 0], 3)
    [0, 0, 0, 1, -2]
    >>> shift([1, -2, 1, 0, 0], -1)
    [-2, 1, 0, 0, 0]
    """
    queue = deque(array)
    if shift_amount < 0:
        queue.reverse()

    for _ in range(abs(shift_amount)):
        queue.pop()
        queue.appendleft(0)

    if shift_amount < 0:
        queue.reverse()

    return list(queue)


def bead_matrix(dimension=5):
    """Return the matrix corresponding to a system of beads on a string.

    Arguments:
        dimension: the number of beads, at least 4

    Returns:
        A dimension-by-dimension numpy matrix representing the linear system.
    """
    if dimension < 4:
        raise ValueError("dimension must be at least 4")
    base = [1, -2, 1] + [0] * (dimension - 3)
    return numpy.array([shift(base, i) for i in range(-1, dimension - 1)])


def sorted_eigensystem(matrix, top_k=None):
    """Compute the eigensystem of the given matrix, sorted by eigenvalue.

    Arguments:
        matrix: an n-by-n matrix
        top_k: the number of eigenvectors to compute. If None, k is set to n.

    Returns:
        A pair (values, vectors) where values is a list of top_k
        eigenvalues, sorted from largest to smallest, and vectors
        is a list of the corresponding eigenvectors.
    """
    top_k = top_k or len(matrix)
    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)

    # sort the eigenvectors by eigenvalue from largest to smallest
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # return eigenvalues as rows of a matrix instead of columns
    return eigenvalues[:top_k], eigenvectors.T[:top_k]


def decompose(eigenvectors, vector):
    """Decompose the given vector in terms of the given eigenvectors.

    Arguments:
        eigenvectors: a list of eigenvectors to use as a basis.
        vector: the vector to decompose.

    Returns:
        A dict d of type {index: coefficient} so that the input vector is equal to
        sum(d[i] * eigenvectors[i] for i in range(len(vector))).
    """
    coefficients = {}
    for i in range(len(vector)):
        coefficients[i] = numpy.dot(vector, eigenvectors[i])

    return coefficients
