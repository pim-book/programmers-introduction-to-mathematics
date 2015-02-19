from polynomial import Polynomial


# pts is a list of (float, float)
# i is an integer idex of pts.
# Return one term from the sum in the construction of Theorem 1 (Chapter 2)
def singleTerm(pts, i):
   theTerm = Polynomial([1.])
   xi, yi = pts[i]

   for j, p in enumerate(pts):
      if j == i:
         continue

      xj = p[0]
      theTerm = theTerm * Polynomial([-xj / (xi - xj), 1.0/(xi - xj)])

   return theTerm * Polynomial([yi])


# pts is a list of (float, float)
# Return the unique degree n polynomial that passes through the given n+1
# points.
def interpolate(pts):
   if len(pts) == 0:
      raise Exception('Must provide at least one point.')

   xValues = [p[0] for p in pts]
   if len(set(xValues)) < len(xValues):
      raise Exception('Not all x values are distinct.')

   terms = [singleTerm(pts, i) for i in range(0, len(pts))]
   return sum(terms, Polynomial([]))


if __name__ == "__main__":
   pts1 = [(1,1)]
   pts2 = [(1,1), (2,0)]
   pts3 = [(1,1), (2,4), (7,9)]

   f = interpolate(pts3)
   print([f(xi) for xi,yi in pts3]) # rounding error, but good enough
