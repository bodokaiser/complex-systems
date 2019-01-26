import numpy as np


def delay(x, k, m):
  # number of embedded coordinates
  l = len(x) - m * k + 1

  # l embeddings, m coordinates
  X = np.zeros((l, m))

  for i, j in enumerate(range(l)):
    X[i] = x[j:j + m * k]

  return X
