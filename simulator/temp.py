import numpy as np
import math
from scipy.integrate import quad, dblquad
from matplotlib.pylab import *

D = 9
m = 0
lmda = 0.1
sigma = 10

def f(x):
    if x < D:
        return 0
    return lmda ** 2 * (x - D) * np.exp(-lmda*(x - D))


def gauss(x):
    return 1 / math.sqrt(2 * 3.141592) / sigma * np.exp(-(x-m)**2/2/sigma**2)


def Q(x):
    def tmp(t):
        return 1/math.sqrt(2*3.141592)*math.exp(-t**2/2)
    return quad(tmp, x, np.inf)[0]


def g(x):
    return lmda ** 2 / math.sqrt(2 * 3.141592) / sigma * math.exp(lmda/2*(2*D+2*m+sigma**2*lmda-2*x)) * (
        sigma ** 2 * math.exp(-(D+m+lmda*sigma**2-x)**2/2/sigma**2) + \
        sigma * (x-D-m-lmda*sigma**2) * math.sqrt(2*3.141592)*Q(-(x-D-m-lmda*sigma**2)/sigma)
    )


def main(x):
    def tmp(tau):
        return f(tau) * gauss(x - tau)
    return quad(tmp, D, np.inf)[0]

if __name__ == "__main__":
    a = np.linspace(-100, 100, 1000)
    b = map(main, a)
    plot(a, b)
    show()

