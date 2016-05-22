import sys
import os
import random
import numpy as np
from numpy.linalg import norm

from simulator.afterQuantization.config import GlobalConfigure
from scipy.optimize import fsolve

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
            if random.random() > p_normal and random.random > config.get_phi_0():
                return 1
            else:
                return 0
        else:
            if random.random() > p_normal and random.random > config.get_phi_1():
                return 0
            else:
                return 1
    quantized_value = map(quantize, data)
    return sum(quantized_value) / float(len(quantized_value))


def main():
    data = load_data(1000)
    threshold = config.get_threshold()
    percent = map(lambda x: count_percentage(data, x, config.get_normal_percentages()), threshold)
    print percent

    def equation(input_param):
        phi_0_to_estimate, phi_1_to_estimate, d = input_param
        # diff = map(lambda x: equation_to_solve(x, percent, phi_0_to_estimate, phi_1_to_estimate, d), threshold)
        diff = equation_to_solve(threshold, percent, phi_0_to_estimate, phi_1_to_estimate, d)
        return diff

    print fsolve(equation, [1, 1, 10])


if __name__ == "__main__":
    main()
