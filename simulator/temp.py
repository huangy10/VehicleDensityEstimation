import numpy as np
import math
from scipy.integrate import quad, dblquad
from matplotlib.pylab import *

m = 25
lmda = 0.1

def f(x, D=9):
    if x < D:
        return 0
    return lmda ** 2 * (x - D) * np.exp(-lmda*(x - D))


def gauss(x, m=25, sigma=10):
    return 1 / math.sqrt(2 * 3.141592) / sigma * np.exp(-(x-m)**2/2/sigma**2)


def g(x, D=9, m=25, sigma=10):
    def tmp(tau):
        return f(tau, D=D) * gauss(x - tau, m=m, sigma=sigma)
    return quad(tmp, D, np.inf)[0]


def G(x):
    return quad(g, -np.inf, x)

tau_set = np.arange(10, 60)

if __name__ == "__main__":
    a = np.linspace(-20, 100, 1000)
    b = map(g, a)
    plot(a, b)
    show()

