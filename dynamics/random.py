import numba

from random import gauss


@numba.jit(nopython=True)
def autoregression(x0, a, b, N, mu=0, sigma=1):
  x = [x0]

  for i in range(1, N + 1):
    x.append(a + b * x[-1] + gauss(mu, sigma))

  return x
