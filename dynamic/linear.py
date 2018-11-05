import numpy as np

from numeric import ode_naive


def romance(R0, J0, a, b, c, d, N, h):
  """Romance dynamics between Romeo and Juliet."""
  x = ode_naive(np.array([R0, J0]), np.array([[a, b], [c, d]]), N, h)

  return x.T[0], x.T[1]
