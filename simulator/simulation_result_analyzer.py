# coding=utf-8

import sys
import os

import numpy as np
from django.core.wsgi import get_wsgi_application
from django.db.models.query import QuerySet

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

from VehicleDataORM.models import Record, Road, Vehicle
from simulator.models import SimulationRecord


def mean_absolute_error(data):
    """ 计算输入数据的平均绝对误差
    """
    if isinstance(data, QuerySet):
        # 如果输入数据是django的QuerySet格式的，将其重新整理为列表
        data = map(lambda x: (x.real_value, x.estimate_value), list(data))

    def absolute_error(a, b):
        return a + np.abs(b[0] - b[1])

    return reduce(absolute_error, data, 0) / len(data)


def mean_relative_error(data):
    """ 计算输入数据的相对误差
    """
    if isinstance(data, QuerySet):
        data = map(lambda x: (x.real_value, x.estimate_value), list(data))

    def relative_error(a, b):
        return a + np.abs(b[0] - b[1]) / b[0]

    return reduce(relative_error, data, 0) / len(data)


