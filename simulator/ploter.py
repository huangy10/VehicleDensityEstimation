# coding=utf-8
# 这个文件的作用是将仿真结果图片绘制出来
import matplotlib.pyplot as plt
from scipy.io import savemat
import os

from simulator.models import SimulationRecord
from simulator.simulation_result_analyzer import mean_absolute_error, mean_relative_error

probe_based_name = 'probe_loss'     # 基于探针方法的仿真结果数据集的名称
distance_based_name = 'distance_loss'   # 基于测距的方法的仿真结果的数据集的名称


def probe_based_plotter():
    loss_set = SimulationRecord.objects.filter(estimation_method=probe_based_name)\
        .distinct('loss_rate').values_list('loss_rate', flat=True)
    err = []
    for l in loss_set:
        data = SimulationRecord.objects.filter(estimation_method=probe_based_name,
                                               loss_rate__range=(l-0.001, l+0.001))
        err.append(mean_relative_error(data))
    plt.plot(loss_set, err, color='red')
    plt.show()


def distance_based_plotter():
    loss_set = SimulationRecord.objects.filter(estimation_method=distance_based_name)\
        .distinct('loss_rate').values_list('loss_rate', flat=True)
    err = []
    for l in loss_set:
        data = SimulationRecord.objects.filter(estimation_method=distance_based_name,
                                               loss_rate__range=(l-0.001, l+0.001))
        err.append(mean_relative_error(data))
    plt.plot(loss_set, err, color='red')
    plt.show()


def save_simulation_result_to_mat():
    output = {}
    loss_set = SimulationRecord.objects.filter(estimation_method=probe_based_name)\
        .distinct('loss_rate').values_list('loss_rate', flat=True)
    err = []
    for l in loss_set:
        data = SimulationRecord.objects.filter(estimation_method=probe_based_name,
                                               loss_rate__range=(l-0.001, l+0.001))
        err.append(mean_relative_error(data))
    print type(list(loss_set))
    output['probe_loss_set'] = list(loss_set)
    output['probe_rel_err'] = err
    loss_set = SimulationRecord.objects.filter(estimation_method=distance_based_name)\
        .distinct('loss_rate').values_list('loss_rate', flat=True)
    err = []
    for l in loss_set:
        data = SimulationRecord.objects.filter(estimation_method=distance_based_name,
                                               loss_rate__range=(l-0.001, l+0.001))
        err.append(mean_relative_error(data))
    output['distance_loss_set'] = list(loss_set)
    output['distance_rel_err'] = err
    print "writing to .mat file"
    savemat('simulator/data/data.mat', output, appendmat=False)
