from numpy.linalg import svd
import numpy as np

movieRatings = [
    [2, 5, 3],
    [1, 2, 1],
    [4, 1, 1],
    [3, 5, 2],
    [5, 3, 1],
    [4, 5, 5],
    [2, 4, 2],
    [2, 2, 5],
]

U, singularValues, V = svd(movieRatings)

print(U)
print(singularValues)
print(V)

Sigma = np.vstack([
    np.diag(singularValues),
    np.zeros((5, 3)),
])

print(np.round(movieRatings - np.dot(U, np.dot(Sigma, V)), decimals=10))


U, singularValues, V = svd(movieRatings, full_matrices=False)
print(U)
print(singularValues)
print(V)

Sigma = np.diag(singularValues)
print(np.round(movieRatings - np.dot(U, np.dot(Sigma, V)), decimals=10))
