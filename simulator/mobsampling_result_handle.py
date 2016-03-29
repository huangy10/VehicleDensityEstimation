# coding=utf-8
import os
import sys
import numpy as np

from django.core.wsgi import get_wsgi_application

sys.path.extend([os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

from VehicleDataORM.models import Road, Record, Vehicle
from simulator.models import SimulationRecord


def mean_absolute_error(data):
    if not data.exists():
        print "没有找到仿真数据"
        return
    data = map(lambda x: (x.real_value, x.estimate_value), list(data))

    def absolute_error(a, b):
        return a + np.abs(b[0] - b[1])

    return reduce(absolute_error, data, 0) / len(data)


def mean_relative_error(data):
    if not data.exists():
        print "没有找到仿真数据"
        return
    data = map(lambda x: (x.real_value, x.estimate_value), list(data))

    def mean_error(a, b):
        return a + np.abs(b[0] - b[1]) / b[0]

    return reduce(mean_error, data, 0) / len(data)


def main():
    pass

if __name__ == '__main__':
    main()
