# coding=utf-8
from django.db import models


class SimulationRecord(models.Model):
    road = models.ForeignKey("VehicleDataORM.Road", verbose_name='对应的spacing表单')
    frame_id = models.IntegerField(default=0, verbose_name='帧id')
    lane_pos = models.IntegerField(default=0, verbose_name='车道位置')

    estimate_value = models.FloatField(default=0, verbose_name='估计值')
    real_value = models.FloatField(default=0, verbose_name='实际值')

    estimation_method = models.CharField(max_length=50, verbose_name='估计方法的名称')
    z = models.FloatField(default=300, verbose_name='通信距离')
    extra_params = models.CharField(max_length=255, verbose_name='额外参数信息', default='')

    created_at = models.DateTimeField(auto_now_add=True)
