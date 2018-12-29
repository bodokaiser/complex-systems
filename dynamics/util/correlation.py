import numba


@numba.jit(nopython=True)
def sum_1d(x, eps):
  C = 0
  N = len(x)

  for i in range(N):
    for j in range(i, N):
      d = (x[i] - x[j])**2

      if d**0.5 < eps:
        C += 1

  return 2 * C / (N * (N - 1))


@numba.jit(nopython=True)
def sum_2d(x, y, eps):
  C = 0
  N = len(x)

  for i in range(N):
    for j in range(i, N):
      d = (x[i] - x[j])**2 + (y[i] - y[j])**2

      if d**0.5 < eps:
        C += 1

  return 2 * C / (N * (N - 1))


@numba.jit(nopython=True)
def sum_3d(x, y, z, eps):
  C = 0
  N = len(x)

  for i in range(N):
    for j in range(i, N):
      d = (x[i] - x[j])**2 + (y[i] - y[j])**2 + (z[i] - z[j])**2

      if d**0.5 < eps:
        C += 1

  return 2 * C / (N * (N - 1))
