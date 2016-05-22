import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pylab
from .config import GlobalConfigure


def equation_to_solve(tau, b, phi_0, phi_1, d):
    return p_after_attack(tau, phi_0, phi_1, d) - b


def p_after_attack(x, phi_0, phi_1, d):
    config = GlobalConfigure()
    p_normal = config.get_normal_percentages()
    pmf = p_before_attack(x, d, config.get_lmda())
    return (p_normal + (1 - p_normal) * phi_0) * pmf + (p_normal * (1 - p_normal) * (1-phi_1)) * (1 - pmf)


def p_before_attack(x, d, lmda):
    diff = np.array([x - d, np.zeros(len(x))]).max(axis=0)
    return 1 - lmda * (diff - 1 / lmda) * np.exp(-lmda * diff)



def main():
    pass


if __name__ == '__main__':
    main()
