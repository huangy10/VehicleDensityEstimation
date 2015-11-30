import numpy as np
import math
from matplotlib.pylab import *
from scipy.integrate import quad

a = 100
sigma = 10

def Q(x):
    def tmp(t):
        return 1/math.sqrt(2*3.141592)*math.exp(-t**2/2)
    return quad(tmp, -np.inf, x)[0]


def f(x):
    return x * math.exp(-(x+a) ** 2/2/sigma**2)


def f1(x):
    return (x-a) * math.exp(-x ** 2/2/sigma**2)


def t(x):
    return x * math.exp(-x**2/2/sigma**2)


def g(x):
    return - a * math.exp(-x**2/2/sigma**2)

def trans_f(x):
    return sigma ** 2 * math.exp(-a**2/2/sigma**2) - g(x)
    #return sigma ** 2 * math.exp(-a**2/2/sigma**2)-a * math.exp(-x**2/2/sigma**2)
    # return x * math.exp(-x**2/2/sigma**2)-a * math.exp(-x**2/2/sigma**2)


if __name__ == "__main__":
    print quad(t, a, np.inf)
    print sigma ** 2 * math.exp(-a**2/2/sigma**2)
    print quad(g, a, np.inf)
    print quad(f, 0, np.inf)
    print quad(f1, a, np.inf)
    print quad(trans_f, a, np.inf)
