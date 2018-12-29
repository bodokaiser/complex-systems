import numpy as np

from scipy.optimize import fmin
from scipy.stats import kurtosis
from scipy.special import lambertw

"""
The algorithm is based on [1]. The implementation is based on [2].

[1]: Georg Goergg, 2013 (https://arxiv.org/pdf/1010.2265.pdf)
[2]: Greg Ver Steeg, 2015 (https://github.com/gregversteeg/gaussianize)
"""


def estimate_parameters(x):
  return np.array([igmm(x_i) for x_i in x.T])


def transform(x, parameters):
  return np.array([
      lambertw_tau(x_i, tau_i) for x_i, tau_i in zip(x.T, parameters)
  ]).T


def inverse_transform(y, parameters):
  return np.array([
      inverse(y_i, tau_i) for y_i, tau_i in zip(y.T, parameters)
  ]).T


def lambertw_delta(z, delta):
  """Lambertw delta function as defined in (9)."""
  if delta < 1e-6:
    return z

  return np.sign(z) * np.sqrt(np.real(lambertw(delta * z ** 2)) / delta)


def lambertw_tau(y, tau):
  """Lambertw tau function as defined in (8)."""
  return tau[0] + tau[1] * lambertw_delta((y - tau[0]) / tau[1], tau[2])


def inverse(x, tau):
  """Inverse distribution transform as defined in (6)."""
  u = (x - tau[0]) / tau[1]

  return tau[0] + tau[1] * (u * np.exp(u * u * (tau[2] * 0.5)))


def igmm(y, tol=1.22e-4, max_iter=100):
  if np.std(y) < 1e-4:
    return np.mean(y), np.std(y).clip(1e-4), 0
  delta0 = delta_init(y)
  tau1 = (np.median(y), np.std(y) * (1. - 2. * delta0) ** 0.75, delta0)
  for k in range(max_iter):
    tau0 = tau1
    z = (y - tau1[0]) / tau1[1]
    delta1 = delta_gmm(z)
    x = tau0[0] + tau1[1] * lambertw_delta(z, delta1)
    mu1, sigma1 = np.mean(x), np.std(x)
    tau1 = (mu1, sigma1, delta1)

    if np.linalg.norm(np.array(tau1) - np.array(tau0)) < tol:
      break
    else:
      if k == max_iter - 1:
        print(f'Warning: No convergence after {max_iter} iterations.')
  return tau1


def delta_gmm(z):
  delta0 = delta_init(z)

  def func(q):
    u = lambertw_delta(z, np.exp(q))
    if not np.all(np.isfinite(u)):
      return 0.
    else:
      k = kurtosis(u, fisher=True, bias=False)**2
      if not np.isfinite(k) or k > 1e10:
        return 1e10
      else:
        return k

  res = fmin(func, np.log(delta0), disp=0)
  return np.around(np.exp(res[-1]), 6)


def delta_init(z):
  gamma = kurtosis(z, fisher=False, bias=False)
  with np.errstate(all='ignore'):
    delta0 = np.clip(1. / 66 * (np.sqrt(66 * gamma - 162.) - 6.), 0.01, 0.48)
  if not np.isfinite(delta0):
    delta0 = 0.01
  return delta0
