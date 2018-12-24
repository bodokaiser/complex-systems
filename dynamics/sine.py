import math
import numba as nb


@nb.jit(nopython=True)
def sine_map(x0, r, n):
  x = [x0]

  for i in range(n):
    x.append(r * math.sin(math.pi * x[-1]))

  return x
