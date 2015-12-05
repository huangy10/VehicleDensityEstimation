# !coding=utf-8
import numpy as np
import math
from scipy.integrate import quad
from matplotlib.pylab import *
from scipy.io import savemat

""" 这个文件使用数值计算的方法来计算在Gauss-offset Attack的情况下CRB与量化门限tau之间的关系
"""

d = 9
m = 25
sigma = 5
lmda = 0.1
N = 2018


def f_pdf(x):
    """ 无攻击情况下车间距分布的密度函数(pdf)
    """
    if x < d:
        return 0
    return lmda ** 2 * (x - d) * math.exp(-lmda * (x - d))


def f_cdf(x):
    """ 无攻击情况下车间距分布的累积分布函数(cdf)
    """
    return lmda * (x - d + 1/lmda) * math.exp(-lmda * (x - d))


def gauss_pdf(x):
    """ 高斯偏移的密度函数(pdf)
    """
    return 1 / math.sqrt(2 * 3.141592) / sigma * math.exp(-(x - m) ** 2 / 2 / sigma ** 2)


def f_pdf_under_attack(x):
    """ 在受到攻击的情况下车间距分布的密度函数
    """
    return quad(lambda tau: f_pdf(tau) * gauss_pdf(x - tau), d, np.inf)[0]


def f_cdf_under_attack(x):
    """ 在受到攻击的情况下车间距分布的累积分布函数
    """
    return quad(f_pdf_under_attack, -np.inf, x)[0]


def f_g_cdf(x, p=0.5):
    """ 贝叶斯公式展开的在有比例为p的车辆没有被攻击的情况下车间距数据的分布
    """
    return p * f_cdf(x) + (1 - p) * f_cdf_under_attack(x)


def p_g(x, p=0.5):
    """ 使用量化门限量化之后大于x的比例
    """
    return 1 - f_g_cdf(x, p)


# def p_g_dd(x, p=0.5):
#     """ 对p_g进行求导
#     """
#     def p_g_pdf_dd(tau):
#         return quad(lambda a: f_pdf(a) * gauss_pdf(tau-a) * (tau-a-m)/sigma**2, d, np.inf)
#
#     return p * f_pdf(x) - (1 - p) * quad(p_g_dd, -np.inf, x)


def phi_gradient(x, p=0.5):

    def p_g_pdf_dm(tau):
        return quad(lambda a: f_pdf(a) * gauss_pdf(tau-a) * (tau-a-m)/sigma**2, d, np.inf)[0]

    p_g_dm = (p - 1) * quad(p_g_pdf_dm, -np.inf, x)[0]
    p_g_dd = p * f_pdf(x) + p_g_dm

    def p_g_pdf_d_sigma(tau):
        return quad(lambda a: f_pdf(a) * gauss_pdf(tau - a) * (-1/sigma + 1 / sigma ** 2 * (tau - a - m) ** 2), d, np.inf)[0]

    p_g_dsigma = (p - 1) * quad(p_g_pdf_d_sigma, -np.inf, x)[0]

    return p_g_dm, p_g_dd, p_g_dsigma


def coefficient(x, p=0.5):
    return N / (p_g(x, p) * (1 - p_g(x, p)))


def J(x, p=0.5):
    vector = list(phi_gradient(x, p))
    vector = np.matrix(vector)
    return coefficient(x, p) * vector.transpose() * vector


tau_set = np.linspace(20, 60, 50)

def main(pp=0.5):

    def get_crb(tau, p):
        fim = J(tau, p) + J(tau+5, p) + J(tau+10, p)
        return np.linalg.inv(fim)[0, 0]

    return map(lambda x: get_crb(x, pp), tau_set)


if __name__ == "__main__":
    result1 = main(0.3)
    result2 = main(0.9)
    print "finished"
    savemat('./data/fig4_data.mat', {
        'tau_set': tau_set,
        'result1': result1,
        'result2': result2,
    })
    # plot(tau_set, result)
    # show()