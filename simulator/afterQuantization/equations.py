import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pylab
from simulator.afterQuantization.config import GlobalConfigure


def equation_to_solve(
        tau, b, phi_0, phi_1, d,
        p_normal=GlobalConfigure().get_normal_percentages(),
        lmda=GlobalConfigure().get_lmda()):
    return p_after_attack(tau, phi_0, phi_1, d, p_normal, lmda) - b


def p_after_attack(x, phi_0, phi_1, d, p_normal, lmda):
    pmf = p_before_attack(x, d, lmda)
    return (p_normal + (1 - p_normal) * phi_0) * pmf + ((1 - p_normal) * (1-phi_1)) * (1 - pmf)


def p_before_attack(x, d, lmda):
    result = 1 - lmda * ((x-d) + 1 / lmda) * np.exp(-lmda * (x-d))
    result *= (x-d) > 0
    return result


def main():
    pass


if __name__ == '__main__':
    main()
