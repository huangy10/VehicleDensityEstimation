# coding=utf-8
import threading
import Queue
import sys
import os
import getopt
import random

import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.optimize import curve_fit, fsolve

from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ValidationError

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

from VehicleDataORM.models import Record, Road, Vehicle

from simulator.models import SimulationRecord
from runner_probe import Manager as ProbeManager


__author__ = 'Woody Huang'
__version__ = '1.0.0'

#  首先估计lambda


def lmda_estimator(road_index=0, sample_pos=500, sample_range=20, r=100):
    """ 这个函数实现对λ参数的估计

     :param road_index  选择使用哪个数据集进行仿真
     :param sample_pos  采样的数据点
     :param sample_range  允许的离采样数据点的偏移(前后)

     :return 返回估计得到的λ的值
    """
    # 首先求出车间距的经验分布cdf
    road = Road.objects.all()[road_index]
    records = Record.objects.filter(road=road, local_y__gt=sample_pos-sample_range,
                                    local_y__lt=sample_pos+sample_range, spacing_m__gt=0, spacing_m__lt=r)\
        .values_list('spacing_m', flat=True)
    ecdf = ECDF(records)
    # 进行曲线拟合求出λ
    y = ecdf(records)

    def F(x, lmda, D):
        return 1 - lmda * (x - D + 1/lmda) * np.exp(-lmda * (x - D))

    result = curve_fit(F, records, y)
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


def d_estimator(lmda, data, thresholds, r=100, loss_rate=0):
    """ 这个函数在已知λ的情况下，实现对参数D的估计，从而可以得到平均车距

     :param lmda    已经得到的λ估计值
     :param data    进行本次估计的数据集
     :param thresholds      量化门限
     :param r       最大探测距离，超过这一部分的距离的会被忽略

     :return        针对各个量化门限给出的估计值
    """
    data = filter(lambda x: (x < r and random.random() >= loss_rate), data)
    data = filter(lambda x: x > 0, data)
    num = len(data)
    if num <= 0:
        return -1

    def estimator(tau):
        l0 = len(filter(lambda x: x < tau, data))

        def F(d):
            """ 待求解的方程的表达式
            """
            return 1 - lmda * (tau - d + 1/lmda) * np.exp(-lmda * (tau - d)) - l0/float(num)

        result = fsolve(F, 0)
        return result[0]

    try:
        return map(estimator, thresholds)
    except TypeError:
        return estimator(thresholds)


class Worker(threading.Thread):

    def __init__(self, R, lmda, road, manager, thresholds, method_name='distance_based_m', loss_rate=[]):
        """
         :param R       雷达的探测距离
         :param lmda    已经估计得到的λ值
         :param road    使用的数据集的类别
         :param manager 所述的调度者
         :param thresholds  尝试的判决门限集，可以是list，也可以是单独的float值
        """
        super(Worker, self).__init__()
        self.working_queue = Queue.Queue()      # Create the queue for the worker
        self.R = R      # Radar detect range
        self.lmda = lmda    # lmda
        self.manager = manager
        self.road = road
        self.thresholds = thresholds
        self.method_name = method_name
        self.loss_rate = loss_rate

    def start(self):
        print "====>Worker %s starts" % self.name
        return super(Worker, self).start()

    def run(self):
        while True:
            if self.working_queue.qsize() == 0 and self.manager.loading_finished:
                break
            package = self.working_queue.get()
            self.estimator(package)
            self.working_queue.task_done()

        print "====>Worker %s finished" % self.name

    def estimator(self, data):
        if len(data) == 0:
            return

        def estimate_single_lane(data_single_lane, thresholds, loss_rate):
            d = d_estimator(self.lmda, data_single_lane, thresholds, r=self.R, loss_rate=loss_rate)
            if d == -1:
                return 0
            try:
                return map(lambda x: 1 / (x + 2/self.lmda), d)
            except TypeError:
                return 1 / (d + 2/self.lmda)

        def data_re_organizer(raw_data, lane_num=4):
            """ 这个函数将同一帧内的数据按照车道分开
             :param raw_data    原始数据，注意这个数据应当是属于同一帧的
             :param lane_num
            """
            place_holder = []
            for _ in range(lane_num):
                place_holder.append([])
            cur_frame_id = raw_data[0].frame_id
            for record in raw_data:
                if cur_frame_id != record.frame_id:
                    raise ValidationError(code='0000', message='数据格式错误，分给Worker的数据包中的数据应当是同一帧的')
                if record.lane_pos <= lane_num:
                    place_holder[record.lane_pos - 1].append(record)
            return place_holder

        cur_frame = data[0].frame_id
        data = data_re_organizer(data)          # 数据重整
        if cur_frame == 9466:
            print data[2]
        for (lane_pos, a) in enumerate(data):
            if len(a) == 0:
                continue
            spacing_data = map(lambda x: x.spacing_m, a)
            for l in self.loss_rate:
                estimated_values = estimate_single_lane(spacing_data, self.thresholds, loss_rate=l)
                for (estimated_value, threshold) in zip(estimated_values, self.thresholds):
                    if estimated_value == 0:
                        continue
                    SimulationRecord.objects.create(
                        road=self.road,
                        frame_id=cur_frame,
                        lane_pos=lane_pos+1,
                        estimate_value=estimated_value,
                        real_value=len(a)/self.road.road_length_m,
                        estimation_method=self.method_name,
                        z=self.R,
                        loss_rate=l,
                        extra_params='threshold:%s' % threshold
                    )


class Manager(ProbeManager):

    def __init__(self, R=100, road_index=0, thresholds=30, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.R = R
        self.road_index = road_index
        self.thresholds = thresholds
        self.lmda = 0

    def start(self):
        print """
        ============================Simulation Starts=========================
        The settings are:
            worker number   :   %s
            data loader     :   %s
        The initial parameters includes:
            DataSet         :   %s
            R               :   %s
            thresholds      :  %s
        ======================================================================
        """ % (self.worker_num, 1, self.road.name, self.R, self.thresholds)
        print "====>Estimating λ"
        self.lmda = lmda_estimator(self.road_index, r=self.R)
        return super(Manager, self).start()

    def create_workers(self, **kwargs):
        for i in range(self.worker_num):
            worker = Worker(R=self.R, lmda=self.lmda, road=Road.objects.all()[self.road_index],
                            manager=self, thresholds=self.thresholds, loss_rate=self.loss_rate,
                            method_name=self.method_name)
            worker.name = str(i)
            self.workers.append(worker)


def parse_command_line_params():
    opt, args = getopt.getopt(sys.argv[1:], "w:r:f:m:t:i:l:")
    raw_param = dict()
    for op, value in opt:
        raw_param[op] = value
    print raw_param
    param = dict()
    if '-t' in raw_param:
        z_str = raw_param['-t']
        if ':' in z_str:
            z_params = map(lambda x: int(x), z_str.split(':'))
            if len(z_params) == 2:
                param['thresholds'] = range(z_params[0], z_params[1])
            else:
                param['thresholds'] = range(z_params[0], z_params[1], z_params[2])
        else:
            param['thresholds'] = [int(raw_param['-t']), ]
    else:
        param['thresholds'] = [30, ]

    def float_range(a, b, step=0.1):
        result = []
        while a < b:
            result.append(a)
            a += step
        return result

    if '-l' in raw_param:
        l_str = raw_param['-l']
        if ':' in l_str:
            l_params = map(lambda x: float(x), l_str.split(':'))
            if len(l_params) == 2:
                param['loss_rate'] = float_range(l_params[0], l_params[1])
            else:
                param['loss_rate'] = float_range(l_params[0], l_params[1], l_params[2])
        else:
            param['loss_rate'] = [float(raw_param['-l']), ]
    else:
        param['loss_rate'] = [0, ]

    param['worker_num'] = int(raw_param.get('-w', 5))
    param['frame_per_fetch'] = int(raw_param.get('-f', 500))
    param['R'] = int(raw_param.get('-r', 100))
    param['method_name'] = raw_param.get('-m', 'test')
    param['road_index'] = int(raw_param.get('-r', 0))
    print param
    return param


if __name__ == '__main__':
    param = parse_command_line_params()
    manager = Manager(**param)
    manager.start()
    manager.join()
    if param['method_name'].startswith('test'):
        print "\n\n\n自动清除本次仿真创建的结果数据"
        SimulationRecord.objects.filter(estimation_method=param['method_name']).delete()
    print "\n仿真完成"
