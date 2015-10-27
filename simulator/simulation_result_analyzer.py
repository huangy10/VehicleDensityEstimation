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
        data = map(lambda x: (x.real_value, x.estimate_value), list(data))

    def absolute_error(a, b):
        return a + np.abs(b[0] - b[1])

    return reduce(absolute_error, data, 0) / len(data)


if __name__ == '__main__':
    data = SimulationRecord.objects.filter(estimation_method='probe_based_method_m', z=2000)
    error = mean_absolute_error(data)
    print error
