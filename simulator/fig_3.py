import numpy as np
import math
from matplotlib.pylab import *
from scipy.io import savemat

D = 9
m = 25
lmda = 0.1
N = 2018
# tau_set = range(30, 40)
tau_set = np.linspace(29.001, 40, 1000)


def F(x):
    if x < D:
        return 0
    else:
        return 1 - lmda * (x - D + 1/lmda) * math.exp(-lmda * (x - D))


def P_F_tau(tau, P=1):
    return 1 - P * F(tau) - (1 - P) * F(tau - m)


def P_F_dD(tau, P=1):
    if tau < D:
        return 0
    if tau - m < D:
        return P * lmda * lmda * (tau - D) * math.exp(-lmda * (tau - D))
    return P * lmda * lmda * (tau - D) * math.exp(-lmda * (tau - D)) + \
        (1 - P) * lmda * lmda * (tau - D - m) * math.exp(-lmda * (tau - D - m))


def P_F_dm(tau, P=1):
    if tau - m <D:
        return 0
    else:
        return (1 - P) * lmda * lmda * (tau - D - m) * math.exp(-lmda * (tau - D - m))


def main():
    P_set = np.linspace(0.1, 0.9, 10)

    tau1_set = tau_set
    result = np.zeros(shape=(len(P_set), len(tau1_set)))
    for (i, P) in enumerate(P_set):
        for (j, tau1) in enumerate(tau1_set):
            tau2 = tau1 + 5
            phi1 = np.matrix([P_F_dD(tau1, P), P_F_dm(tau1, P)])
            phi2 = np.matrix([P_F_dD(tau2, P), P_F_dm(tau2, P)])
            J = N / (1-P_F_tau(tau1, P)) / P_F_tau(tau1, P) * phi1.transpose() * phi1 + \
                N / (1-P_F_tau(tau2, P)) / P_F_tau(tau2, P) * phi2.transpose() * phi2
            # if np.linalg.det(J) <= 1e-5:
            #    continue
            result[i, j] = np.linalg.inv(J)[0, 0]
    return result


if __name__ == '__main__':
    result = main()

    plot(tau_set, result[0], color='red', linestyle='-')
    plot(tau_set, result[3], color='black', linestyle=':')
    plot(tau_set, result[5], color='green', linestyle='--')
    savemat('./data/fig3_data.mat', {
        'tau_set': tau_set,
        'result': result,
        'P': np.linspace(0.1, 0.9, 10)
    }, appendmat=False)
    show()


