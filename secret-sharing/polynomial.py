from itertools import zip_longest


# strip all copies of elt from the end of the list
def strip(L, elt):
    if len(L) == 0:
        return L

    i = len(L) - 1
    while i >= 0 and L[i] == elt:
        i -= 1

    return L[:i+1]


class Polynomial(object):
    def __init__(self, coefficients):
        self.coefficients = strip(coefficients, 0)
        self.indeterminate = 'x'

    def add(self, other):
        newCoefficients = [sum(x)
                           for x in zip_longest(self, other, fillvalue=0.)]
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
        return len(self.coefficients)

    def __repr__(self):
        return ' + '.join(['%s %s^%d' % (a, self.indeterminate, i) if i > 0 else '%s' % a
                           for i, a in enumerate(self.coefficients)])

    def evaluateAt(self, x):
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
