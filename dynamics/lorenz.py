import numpy as np
import numba as nb


@nb.jit(nopython=True)
def u(x, y, a):
  return a * (y - x)


@nb.jit(nopython=True)
def v(x, y, z, b):
  return x * (b - z) - y


@nb.jit(nopython=True)
def w(x, y, z, c):
  return x * y - c * z


@nb.jit(nopython=True)
def naive(x0, y0, z0, a, b, c, N, h):
  x, y, z = [x0], [y0], [z0]

  for i in range(N):
    xi, yi, zi = x[-1], y[-1], z[-1]

    x.append(xi + u(xi, yi, a) * h)
    y.append(yi + v(xi, yi, zi, b) * h)
    z.append(zi + w(xi, yi, zi, c) * h)

  return np.array(x), np.array(y), np.array(z)


@nb.jit(nopython=True)
def rk4(x0, y0, z0, a, b, c, N, h):
  x, y, z = [x0], [y0], [z0]

  for i in range(N):
    xi, yi, zi = x[-1], y[-1], z[-1]

    u1 = h * u(xi, yi, a)
    u2 = h * u(xi + h / 2, yi + u1 / 2, a)
    u3 = h * u(xi + h / 2, yi + u2 / 2, a)
    u4 = h * u(xi + h, yi + u3, a)

    v1 = h * v(xi, yi, zi, b)
    v2 = h * v(xi + h / 2, yi + v1 / 2, a)
    v3 = h * v(xi + h / 2, yi + v2 / 2, a)
    v4 = h * v(xi + h, yi + v3, a)

    w1 = h * w(xi, yi, zi, c)
    w2 = h * w(xi + h / 2, zi + w1 / 2, b, c)
    w3 = h * w(xi + h / 2, zi + w2 / 2, b, c)
    w4 = h * w(xi + h, zi + w3, b, c)

    x.append(xi + u1 / 6 + u2 / 3 + u3 / 3 + u4 / 6)
    y.append(yi + v1 / 6 + v2 / 3 + v3 / 3 + v4 / 6)
    z.append(zi + w1 / 6 + w2 / 3 + w3 / 3 + w4 / 6)

  return np.array(x), np.array(y), np.array(z)
