import numpy as np
import numba as nb


@nb.jit(nopython=True)
def logistic_map(x0, r, n):
  x = [x0]

  for i in range(n):
    x.append(r * x[-1] * (1 - x[-1]))

  return x
