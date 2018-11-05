import numpy as np
import numba as nb


@nb.jit(nopython=True)
def naive(R0, J0, a, b, c, d, N, h):
  R = [R0]
  J = [J0]

  for i in range(N):
    R.append(R[-1] + (a * R[-1] + b * J[-1]) * h)
    J.append(J[-1] + (c * R[-1] + d * J[-1]) * h)

  return np.array(R), np.array(J)
