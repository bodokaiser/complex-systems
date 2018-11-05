import numba as nb
import numpy as np


@nb.jit()
def naive(x0, A, N, h):
  x = [x0]

  for i in range(N):
    x.append(x[-1] + A @ x[-1] * h)

  return np.array(x)
