import numpy as np
import numba as nb


@nb.jit(nopython=True)
def p(y, z):
  return - y - z


@nb.jit(nopython=True)
def q(x, y, a):
  return x + a * y


@nb.jit(nopython=True)
def r(x, z, b, c):
  return b + z * (x - c)


@nb.jit(nopython=True)
def naive(x0, y0, z0, a, b, c, N, h):
  x, y, z = [x0], [y0], [z0]

  for i in range(N):
    xi, yi, zi = x[-1], y[-1], z[-1]

    x.append(xi - p(yi, zi) * h)
    y.append(yi + q(xi, yi, a) * h)
    z.append(zi + r(xi, zi, b, c) * h)

  return np.array(x), np.array(y), np.array(z)


@nb.jit(nopython=True)
def rk4(x0, y0, z0, a, b, c, N, h):
  x, y, z = [x0], [y0], [z0]

  for i in range(N):
    xi, yi, zi = x[-1], y[-1], z[-1]

    u1 = h * p(yi, zi)
    u2 = h * p(yi + h / 2, zi + u1 / 2)
    u3 = h * p(xi + h / 2, zi + u2 / 2)
    u4 = h * p(xi + h, zi + u3)

    v1 = h * q(xi, yi, a)
    v2 = h * q(xi + h / 2, yi + v1 / 2, a)
    v3 = h * q(xi + h / 2, yi + v2 / 2, a)
    v4 = h * q(xi + h, yi + v3, a)

    w1 = h * r(xi, zi, b, c)
    w2 = h * r(xi + h / 2, zi + w1 / 2, b, c)
    w3 = h * r(xi + h / 2, zi + w2 / 2, b, c)
    w4 = h * r(xi + h, zi + w3, b, c)

    x.append(xi + u1 / 6 + u2 / 3 + u3 / 3 + u4 / 6)
    y.append(yi + v1 / 6 + v2 / 3 + v3 / 3 + v4 / 6)
    z.append(zi + w1 / 6 + w2 / 3 + w3 / 3 + w4 / 6)

  return np.array(x), np.array(y), np.array(z)
