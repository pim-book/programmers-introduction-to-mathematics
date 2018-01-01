from collections import deque

import matplotlib.pyplot as plt
import numpy


markers = ['o', 'v', 's', '+', 'x', 'd', 'p', '*']


def shift(array, shift_amount):
    '''
    shift a list right (positive) or left (negative) by a given amount,
    filling new entries with zero.

    >>> shift([1,-2,1,0,0], 1)
    [0,1,-2,1,0]
    >>> shift([1,-2,1,0,0], 3)
    [0,0,0,1,-2]
    >>> shift([1,-2,1,0,0], -1)
    [-2,1,0,0,0]
    '''
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
    if dimension < 4:
        raise Exception("dimension must be at least 4")
    base = [1, -2, 1] + [0] * (dimension - 3)
    return numpy.array([shift(base, i) for i in range(-1, dimension - 1)])


def sorted_eigensystem(matrix, top_k=None):
    top_k = top_k or len(matrix)
    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)

    # sort the eigenvectors by eigenvalue from largest to smallest
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # return eigenvalues as rows of a matrix instead of columns
    return eigenvalues[:top_k], eigenvectors.T[:top_k]


def decompose(eigenvectors, vector):
    # return a dict d:index -> coefficient so that the input vector is equal to
    # sum(d[i] * eigenvectors[i] for i in range(len(vector)))
    coefficients = {}
    for i in range(len(vector)):
        coefficients[i] = numpy.dot(vector, eigenvectors[i])

    return coefficients


def plot_eigenvectors(eigensystem, markersize=6):
    eigenvalues, eigenvectors = eigensystem
    x = numpy.arange(0, len(eigenvectors[0]), 1)
    fig = plt.figure()
    for val, vec, marker in zip(eigenvalues, eigenvectors, markers):
        plt.plot(x, vec, marker=marker, markersize=markersize,
                 label="λ = %G" % val)

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    return fig


def create_and_save_plots():
    A = bead_matrix(5)
    eigensystem = sorted_eigensystem(A)
    eigenvalues, eigenvectors = eigensystem

    print("%s | %s" % ("eigenvalue", "eigenvector"))
    for val, vec in zip(eigenvalues, eigenvectors):
        vec_str = ', '.join(['%5.2f' % entry for entry in vec])
        print("%10.2f | %s" % (val, vec_str))

    fig1 = plot_eigenvectors(eigensystem)
    fig1.savefig("eigenvalues_5_beads.pdf", bbox_inches="tight")

    fig2 = plot_eigenvectors(
        sorted_eigensystem(bead_matrix(100), top_k=5), markersize=4)
    fig2.savefig("eigenvalues_100_beads.pdf", bbox_inches="tight")


if __name__ == "__main__":
    A = bead_matrix(5)
    eigensystem = sorted_eigensystem(A)
    eigenvalues, eigenvectors = eigensystem
    w = [0, 0.5, 0, 0, 0]
    coeffs = decompose(eigenvectors, w)
    reconstructed = numpy.sum(
        [coeffs[i] * eigenvectors[i] for i in range(5)], axis=0)
    print("w={}\nreconstructed={}".format(w, reconstructed))

