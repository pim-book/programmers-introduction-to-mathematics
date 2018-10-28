from itertools import zip_longest


def strip(L, elt):
    '''Strip all copies of elt from the end of the list.

    Arguments:
        L: a list (an indexable, sliceable object)
        elt: the object to be removed

    Returns:
        a slice of L with all copies of elt removed from the end.
    '''
    if len(L) == 0:
        return L

    i = len(L) - 1
    while i >= 0 and L[i] == elt:
        i -= 1

    return L[:i+1]


class Polynomial(object):
    '''A class representing a polynomial as a list of coefficients with no
    trailing zeros.

    A degree zero polynomial corresponds to the empty list of coefficients,
    and is provided by this module as the variable ZERO.

    Polynomials override the basic arithmetic operations.
    '''

    def __init__(self, coefficients):
        '''Create a new polynomial.

        The caller must provide a list of all coefficients of the
        polynomial, even those that are zero. E.g.,
        Polynomial([0, 1, 0, 2]) corresponds to f(x) = x + 2x^3.
        '''
        self.coefficients = strip(coefficients, 0)
        self.indeterminate = 'x'

    def add(self, other):
        newCoefficients = [
            sum(x) for x in zip_longest(self, other, fillvalue=0.)
        ]
        return Polynomial(newCoefficients)

    def __add__(self, other):
        return self.add(other)

    def multiply(self, other):
        newCoeffs = [0] * (len(self) + len(other) - 1)

        for i, a in enumerate(self):
            for j, b in enumerate(other):
                newCoeffs[i+j] += a*b

        return Polynomial(strip(newCoeffs, 0))

    def __mul__(self, other):
        return self.multiply(other)

    def __len__(self):
        '''len satisfies len(p) == 1 + degree(p).'''
        return len(self.coefficients)

    def __repr__(self):
        return ' + '.join(['%s %s^%d' % (a, self.indeterminate, i) if i > 0 else '%s' % a
                           for i, a in enumerate(self.coefficients)])

    def evaluateAt(self, x):
        '''Evaluate a polynomial at an input point.

        Uses Horner's method, first discovered by Persian mathematician
        Sharaf al-Dīn al-Ṭūsī, which evaluates a polynomial by minimizing
        the number of multiplications.
        '''
        theSum = 0

        for c in reversed(self.coefficients):
            theSum = theSum * x + c

        return theSum

    def __iter__(self):
        return iter(self.coefficients)

    def __neg__(self):
        return Polynomial([-a for a in self])

    def __sub__(self, other):
        return self + (-other)

    def __call__(self, *args):
        return self.evaluateAt(args[0])


ZERO = Polynomial([])
