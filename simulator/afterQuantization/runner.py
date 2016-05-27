# coding=utf-8
import sys
import os
import random
import numpy as np
from numpy.linalg import norm
from statsmodels.distributions import ECDF

from simulator.afterQuantization.config import GlobalConfigure
from scipy.optimize import fsolve, curve_fit

from django.core.wsgi import get_wsgi_application

from simulator.afterQuantization.equations import equation_to_solve

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pylab

# Attack parameters
p01 = 1
p10 = 1

from VehicleDataORM.models import Record, Road, Vehicle
from simulator.models import SimulationRecord

config = GlobalConfigure()


def load_data(frame_id):
    r = Road.objects.all().first()
    if isinstance(frame_id, list):
        data = Record.objects.filter(lane_pos=1, frame_id__in=frame_id, road=r)
    else:
        data = Record.objects.filter(lane_pos=1, frame_id=frame_id, road=r)
    return data.values_list("spacing_m", flat=True)


def count_percentage(data, threshold, p_normal):
    """
    :param data: list of Records
    :param threshold: quantization threshold
    :param p_normal: percentage of attack-free vehicles
    :return:
    """
    def quantize(x):
        raw_result = 1 if x > threshold else 0
        if raw_result == 0:
            if random.random() > p_normal and random.random() > config.get_phi_0():
                return 1
            else:
                return 0
        else:
            if random.random() > p_normal and random.random() > config.get_phi_1():
                return 0
            else:
                return 1
    quantized_value = map(quantize, data)
    return 1 - sum(quantized_value) / float(len(quantized_value))


def count_percentage_attack_free(data, threshold):

    def quantize(x):
        return 1 if x > threshold else 0

    quantized_value = map(quantize, data)
    return 1 - sum(quantized_value) / float(len(quantized_value))


def lmda_estimator(data):
    ecdf = ECDF(data)
    y = ecdf(data)

    def F(x, lmda, D):
        return 1 - lmda * (x - D + 1 / lmda) * np.exp(-lmda * (x - D))

    result = curve_fit(F, data, y)
    print """
        ===================λ估计完成，结果如下===================
            λ：%s
            D: %s
            Covariance matrix:
                 | %s\t, %s |
                 | %s\t, %s |
        ======================================================
        """ % (result[0][0], result[0][1], result[1][0][0], result[1][0][1], result[1][1][0], result[1][1][1])

    return result[0][0]


def distance_based_d_estimator(data, threshold):
    quantized = map(lambda x: x > threshold, data)
    percent = 1 - sum(quantized) / float(len(data))

    lmda = GlobalConfigure().get_lmda()

    def F(d):
        if d >= threshold:
            return 0
        return 1 - lmda * (threshold - d + 1/lmda) * np.exp(-lmda * (threshold - d)) - percent

    result = fsolve(F, 0)
    return result[0]


def main():
    data = load_data(range(5900, 6000, 1))
    print len(data)
    GlobalConfigure().lmda = lmda_estimator(data)
    threshold = config.get_threshold()
    percent = map(lambda x: count_percentage(data, x, config.get_normal_percentages()), threshold)
    print percent
    print map(lambda x: count_percentage_attack_free(data, x), threshold)

    print distance_based_d_estimator(data, threshold[1])

    def equation(input_param):
        phi_0_to_estimate, phi_1_to_estimate, d = input_param
        # diff = map(lambda x: equation_to_solve(x, percent, phi_0_to_estimate, phi_1_to_estimate, d), threshold)
        diff = equation_to_solve(threshold, percent, phi_0_to_estimate, phi_1_to_estimate, d)
        print diff, input_param
        return diff

    print fsolve(equation, [1, 1, 10])


def draw_3d_image():
    pass


if __name__ == "__main__":
    main()
