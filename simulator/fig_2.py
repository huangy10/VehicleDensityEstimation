from matplotlib.pylab import *
import numpy as np
import math
from scipy.io import savemat


D = 9
N = 2018
lmda_set = [0.07, 0.10, 0.13]
# tau_set = range(10, 50)
tau_set = np.linspace(9.01, 40, 1000)


def F(x, lmda=0.1):
    if x < D:
        return 0
    else:
        return 1 - lmda * (x - D + 1/lmda) * math.exp(-lmda * (x - D))


def f(x, lmda=0.1):
    if x < D:
        return 0
    else:
        return lmda * lmda * (x - D) * math.exp(-lmda * (x - D))


def main():

    result = np.zeros(shape=(len(lmda_set), len(tau_set)))
    for i, lmda in enumerate(lmda_set):
        for j, tau in enumerate(tau_set):
            result[i, j] = F(tau, lmda) * (1 - F(tau, lmda))/(f(tau, lmda) ** 2 * N)

    return result


if __name__ == "__main__":
    result = main()
    plot(tau_set, result[0], color='red', linestyle='-')
    plot(tau_set, result[1], color='black', linestyle=':')
    plot(tau_set, result[2], color='green', linestyle='--')
    savemat('./data/fig2_data.mat', {
        'tau_set': tau_set,
        'result': result,
        'P': np.linspace(0.1, 0.9, 10)
    }, appendmat=False)
    show()

