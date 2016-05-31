# coding=utf-8
import sys
import os
import random
import numpy as np
from numpy.linalg import norm
from scipy.io import savemat
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

base_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))


def load_data(frame_id):
    r = Road.objects.all().first()
    if isinstance(frame_id, list):
        data = Record.objects.filter(frame_id__in=frame_id, road=r)
    else:
        data = Record.objects.filter(frame_id=frame_id, road=r)
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
    # print """
    #     ===================λ估计完成，结果如下===================
    #         λ：%s
    #         D: %s
    #         Covariance matrix:
    #              | %s\t, %s |
    #              | %s\t, %s |
    #     ======================================================
    #     """ % (result[0][0], result[0][1], result[1][0][0], result[1][0][1], result[1][1][0], result[1][1][1])

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


def real_spacing(data):
    return sum(data) / float(len(data))


def estimator(frame_range, p_normal):
    data = load_data(frame_range)
    # estimate lmda value
    lmda = lmda_estimator(data)
    threshold = config.get_threshold()
    percent = map(lambda x: count_percentage(data, x, p_normal), threshold)

    def equation(input_param):
        phi_0_to_estimate, phi_1_to_estimate, d = input_param
        # phi_0_to_estimate, d = input_param
        diff = equation_to_solve(
            threshold, percent,
            phi_0_to_estimate, phi_1_to_estimate, d,
            p_normal=p_normal,
            lmda=lmda
        )
        # print diff, input_param
        return diff

    phi_0, phi_1, D = fsolve(equation, [1, 0, 10])
    estimate_spacing = D + 2 / lmda
    real_space = real_spacing(data)
    return (estimate_spacing - real_space) / real_space


def estimator_with_data(data, lmda, p_normal):
    threshold = config.get_threshold()
    percent = map(lambda x: count_percentage(data, x, p_normal), threshold)

    def equation(input_param):
        phi_0_to_estimate, phi_1_to_estimate, d = input_param
        # phi_0_to_estimate, d = input_param
        diff = equation_to_solve(
            threshold, percent,
            phi_0_to_estimate, phi_1_to_estimate, d,
            p_normal=p_normal,
            lmda=lmda
        )
        # print diff, input_param
        return diff

    phi_0, phi_1, D = fsolve(equation, [1, 0, 10])
    estimate_spacing = D + 2 / lmda
    real_space = real_spacing(data)
    return min(np.abs(estimate_spacing - real_space) / real_space, 1)


def main():
    savemat(os.path.join(base_path, "data/test.mat"), dict(a=1), appendmat=False)
    p_normals = np.arange(0.5, 1, 0.01)
    frame_start_range = range(0, 9000, 100)

    lmda_index = dict()
    for frame_start in frame_start_range:
        lmda_index[frame_start] = lmda_estimator(load_data(range(frame_start, frame_start + 100)))

    y = []
    for p in p_normals:

        y_temp = map(lambda a: estimator_with_data(load_data(range(frame_start, frame_start + 100)), lmda_index[a], p),
                     frame_start_range)
        y_temp = sum(y_temp) / float(len(y_temp))
        y.append(y_temp)
    #
    # pylab.plot(p_normals, y)
    # pylab.show()

    # write simulation result to mat file
    print "Writing to .mat file"
    savemat(os.path.join(base_path, "data/after_quantization.mat"), dict(
        p_normals=p_normals,
        relative_error=y
    ), appendmat=False)

    # data = load_data(range(4500, 4600, 1))
    # print len(data)
    # GlobalConfigure().lmda = lmda_estimator(data)
    # threshold = config.get_threshold()
    # percent = map(lambda x: count_percentage(data, x, config.get_normal_percentages()), threshold)
    # print percent
    # print map(lambda x: count_percentage_attack_free(data, x), threshold)
    #
    # print distance_based_d_estimator(data, threshold[1])
    #
    # def equation(input_param):
    #     phi_0_to_estimate, phi_1_to_estimate, d = input_param
    #     # phi_0_to_estimate, d = input_param
    #     diff = equation_to_solve(threshold, percent, phi_0_to_estimate, phi_1_to_estimate, d)
    #     # print diff, input_param
    #     return diff
    #
    # phi_0, phi_1, D = fsolve(equation, [1, 0, 10])
    # estimate_spacing = D + 2 / GlobalConfigure().get_lmda()
    # print phi_0, phi_1, D
    # print estimate_spacing, real_spacing(data)


if __name__ == "__main__":
    main()
