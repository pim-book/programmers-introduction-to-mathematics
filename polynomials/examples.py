from polynomial import *
from interpolate import *

f = Polynomial([109, -55, 271])
for i in range(1,6):
   print((i, f(i)))

pts = [(1, 325), (3, 2383), (5, 6609)]
f = interpolate(pts)

print(f)
print(f(0))


pts = [(2, 1083), (5, 6609)]
f = interpolate(pts + [(0, 533)])

print(f)
print(f(0))
