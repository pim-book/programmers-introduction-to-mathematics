from polynomial import Polynomial
from polynomial import ZERO


def single_term(points, i):
    """Return one term of an interpolated polynomial.

    This method computes one term of the sum from the proof of Theorem 2.2.
    In particular, it computes:

      y_i \product_{j=0}^n (x - x_i) / (x_i - x_j)

    The encapsulating `interpolate` function sums these terms to construct
    the final interpolated polynomial.

    Arguments:
      - points: a list of (float, float)
      - i: an integer indexing a specific point

    Returns:
      A Polynomial instance containing the desired product.
    """
    theTerm = Polynomial([1.])
    xi, yi = points[i]

    for j, p in enumerate(points):
        if j == i:
            continue

        xj = p[0]
        
        """
        The inlined Polynomial instance below is how we represent 
        
          (x - x_i) / (x_i - x_j) 
        
        using our Polynomial data type (where t is the variable, and
        x_i, x_j are two x-values of data points):
        
          (x - x_i) / (x_i - x_j) = (-x_j / (x_i - x_j)) * t^0 
                                  +    (1 / (x_i - x_j)) * t^1
        """
        theTerm = theTerm * Polynomial([-xj / (xi - xj), 1.0 / (xi - xj)])

    # Polynomial([yi]) is a constant polynomial, i.e., we're scaling theTerm 
    # by a constant.
    return theTerm * Polynomial([yi])


def interpolate(points):
    """Return the unique degree n polynomial passing through the given n+1 points."""
    if len(points) == 0:
        raise ValueError('Must provide at least one point.')

    x_values = [p[0] for p in points]
    if len(set(x_values)) < len(x_values):
        raise ValueError('Not all x values are distinct.')

    terms = [single_term(points, i) for i in range(0, len(points))]
    return sum(terms, ZERO)
