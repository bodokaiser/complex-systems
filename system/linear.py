import numpy as np
import numba as nb


@nb.jit(nopython=True)
def romance(R0, J0, a, b, c, d, N, dt):
  R = [R0]
  J = [J0]

  for i in range(N):
    R.append(R[-1] + (a * R[-1] + b * J[-1]) * dt)
    J.append(J[-1] + (c * R[-1] + d * J[-1]) * dt)

  return np.array(R), np.array(J)
