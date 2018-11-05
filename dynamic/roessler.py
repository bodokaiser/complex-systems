import numpy as np
import numba as nb


@nb.jit(nopython=True)
def naive(x0, y0, z0, a, b, c, N, h):
  x, y, z = [x0], [y0], [z0]

  for i in range(N):
    xi, yi, zi = x[-1], y[-1], z[-1]

    x.append(xi - (yi + zi) * h)
    y.append(yi + (xi + a * yi) * h)
    z.append(b + (xi - c) * zi * h)

  return np.array(x), np.array(y), np.array(z)
