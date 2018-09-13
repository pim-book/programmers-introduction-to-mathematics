import numpy as np
from numpy.linalg import norm

from random import normalvariate
from math import sqrt


def random_unit_vector(n):
    unnormalized = [normalvariate(0, 1) for _ in range(n)]
    the_norm = sqrt(sum(x * x for x in unnormalized))
    return [x / the_norm for x in unnormalized]


def svd_1d(A, epsilon=1e-10):
    '''Compute the one-dimensional SVD.

    Arguments:
        A: an n-by-m matrix
        epsilon: a tolerance

    Returns:
        the top singular vector of A.
    '''

    n, m = A.shape
    x = random_unit_vector(min(n, m))
    last_v = None
    current_v = x

    if n > m:
        B = np.dot(A.T, A)
    else:
        B = np.dot(A, A.T)

    iterations = 0
    while True:
        iterations += 1
        last_v = current_v
        current_v = np.dot(B, last_v)
        current_v = current_v / norm(current_v)

        if abs(np.dot(current_v, last_v)) > 1 - epsilon:
            print("converged in {} iterations!".format(iterations))
            return current_v


def svd(A, k=None, epsilon=1e-10):
    '''Compute the singular value decomposition of a matrix A using
    the power method.

    Arguments:
        A: an n-by-m matrix
        k: the number of singular values to compute
           If k is None, compute the full-rank decomposition.
        epsilon: a tolerance factor

    Returns:
        A tuple (S, u, v), where S is a list of singular values,
        u is an n-by-k matrix containing the left singular vectors,
        v is a k-by-m matrix containnig the right-singular-vectors
    '''
    A = np.array(A, dtype=float)
    n, m = A.shape
    svd_so_far = []
    if k is None:
        k = min(n, m)

    for i in range(k):
        matrix_for_1d = A.copy()

        for singular_value, u, v in svd_so_far[:i]:
            matrix_for_1d -= singular_value * np.outer(u, v)

        if n > m:
            v = svd_1d(matrix_for_1d, epsilon=epsilon)  # next singular vector
            u_unnormalized = np.dot(A, v)
            sigma = norm(u_unnormalized)  # next singular value
            u = u_unnormalized / sigma
        else:
            u = svd_1d(matrix_for_1d, epsilon=epsilon)  # next singular vector
            v_unnormalized = np.dot(A.T, u)
            sigma = norm(v_unnormalized)  # next singular value
            v = v_unnormalized / sigma

        svd_so_far.append((sigma, u, v))

    singular_values, us, vs = [np.array(x) for x in zip(*svd_so_far)]
    return singular_values, us.T, vs


if __name__ == "__main__":
    movie_ratings = np.array([
        [2, 5, 3],
        [1, 2, 1],
        [4, 1, 1],
        [3, 5, 2],
        [5, 3, 1],
        [4, 5, 5],
        [2, 4, 2],
        [2, 2, 5],
    ], dtype='float64')

    # v1 = svd_1d(movie_ratings)
    # print(v1)

    theSVD = svd(movie_ratings)
