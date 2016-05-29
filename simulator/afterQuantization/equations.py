import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pylab
from simulator.afterQuantization.config import GlobalConfigure


def equation_to_solve(tau, b, phi_0, phi_1, d):
    return p_after_attack(tau, phi_0, phi_1, d) - b


def p_after_attack(x, phi_0, phi_1, d):
    config = GlobalConfigure()
    p_normal = config.get_normal_percentages()
    pmf = p_before_attack(x, d, config.get_lmda())
    return (p_normal + (1 - p_normal) * phi_0) * pmf + ((1 - p_normal) * (1-phi_1)) * (1 - pmf)


def p_before_attack(x, d, lmda):
    result = 1 - lmda * ((x-d) + 1 / lmda) * np.exp(-lmda * (x-d))
    result *= (x-d) > 0
    return result


def main():
    # x = np.arange(0, 100, 0.1)
    # y = p_before_attack(x,  10, GlobalConfigure().get_lmda())
    # z = p_after_attack(x, 0.9, 0.9, 10)
    # pylab.plot(x, y)
    # pylab.plot(x, z)
    # pylab.show()
    xx = np.arange(0, 1, 0.001)
    y = map(lambda x : p_after_attack(30, x, 1, 3.18), xx)
    pylab.plot(xx, y)
    pylab.show()


if __name__ == '__main__':
    main()
