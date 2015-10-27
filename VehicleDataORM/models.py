# coding=utf-8
from django.db import models
from django.utils.encoding import smart_str

# Create your models here.


class Road(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'道路名称')
    description = models.TextField(max_length=255, verbose_name=u'道路信息描述')
    road_length = models.FloatField(default=0)

    road_length_m = models.FloatField(default=0)


class Vehicle(models.Model):
    v_id = models.IntegerField(default=0, verbose_name=u'文件中定义的id')
    road = models.ForeignKey(Road)
    width = models.FloatField(default=0, verbose_name=u'车辆宽度')
    length = models.FloatField(default=0, verbose_name=u'车辆长度')
    name = models.CharField(default=u'', verbose_name=u'车辆名称', max_length=255)
    vehicle_class = models.IntegerField(choices=(
        (1, 'motorcycle'),
        (2, 'auto'),
        (3, 'trunk'),
    ), default=1)


class Record(models.Model):
    description_file = models.FilePathField(null=True)
    vehicle = models.ForeignKey(Vehicle)
    road = models.ForeignKey(Road, db_index=True)

    frame_id = models.IntegerField(default=0, verbose_name=u'帧id', db_index=True)
    global_time = models.BigIntegerField(default=0, verbose_name=u'全局时间')
    local_x = models.FloatField(default=0, verbose_name=u'x')
    local_y = models.FloatField(default=0, verbose_name=u'y', db_index=True)
    local_y_m = models.FloatField(default=0, verbose_name=u'y_in_meters', db_index=True)
    global_x = models.FloatField(default=0, verbose_name=u'全局坐标x')
    global_y = models.FloatField(default=0, verbose_name=u'全局坐标y')
    velocity = models.FloatField(default=0, verbose_name=u'汽车速度')
    acceleration = models.FloatField(default=0, verbose_name=u'汽车加速度')
    lane_pos = models.IntegerField(default=0, verbose_name=u'车道位置')
    preceding_vehicle = models.ForeignKey(Vehicle, related_name='+')
    spacing = models.FloatField(default=0, verbose_name=u'与前车的距离')
    spacing_m = models.FloatField(default=0, verbose_name=u'与前车的距离_in_meters')
    following_vehicle = models.ForeignKey(Vehicle, related_name='+')
    headway = models.FloatField(default=0, help_text=u"""
        Headway provides the time to travel from the front-center of a vehicle (at the speed of the vehicle) to the
        front-center of the preceding vehicle. A headway value of 9999.99 means that the vehicle is traveling at zero
        speed (congested conditions).
    """)

    processed = models.BooleanField(default=False, help_text='这条记录是否已经被处理了')

    def __str__(self):
        return smart_str(str(self.local_y_m))

    class Meta:
        ordering = ('frame_id', )
