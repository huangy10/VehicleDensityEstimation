# coding=utf-8
import sys
import os
import random
from django.core.wsgi import get_wsgi_application

sys.path.extend([os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

from VehicleDataORM.models import Road, Record, Vehicle
from simulator.models import SimulationRecord
from django.db.models import Avg


COMMUNICATE_RANGE = 100.0


def estimate_with_loss(sampler, frame, road, lane_num, loss_rate = 0):
    records = Record.objects.filter(road=road, frame_id=frame)
    real_value = records.count() / road.road_length_m / lane_num
    sample_record = records.filter(vehicle=sampler).first()
    if sample_record is None:
        sampler, sample_record = switch_sampler(sampler, frame, road)
    response_count = 0
    for record in records:
        if 0 < sample_record.local_y_m - record.local_y_m < COMMUNICATE_RANGE and random.random() > loss_rate:
            response_count += 1
    estimated_value = (response_count + 1) / (lane_num * COMMUNICATE_RANGE)
    SimulationRecord.objects.create(
        road=road,
        frame_id=frame,
        lane_pos=-1,
        estimate_value=estimated_value,
        real_value=real_value,
        z=0,
        loss_rate=0,
        estimation_method="mobsampling"
    )
    return sampler


def estimate(sampler, frame, road, lane_num):
    a = None
    for loss in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        a = estimate_with_loss(sampler, frame, road, lane_num, loss)
    return a


def switch_sampler(sampler, frame, road):
    """
     :param sampler Original Sampler
    """
    print "switching sampler: %s" % sampler.id
    records = Record.objects.filter(road=road, frame_id=frame)

    def comparator(a, b):
        if abs(a.local_y_m - COMMUNICATE_RANGE) < abs(b.local_y_m - COMMUNICATE_RANGE):
            return -1
        else:
            return 1
    temp = sorted(records, comparator)[0]
    print "to new sampler: %s at %s " % (temp.vehicle.id, temp.local_y_m)
    return temp.vehicle, temp


def main():
    print "=================Simulation Start===================="
    SimulationRecord.objects.filter(estimation_method="mobsampling").delete()
    road = Road.objects.all()[0]
    lane_num = Record.objects.filter(road=road)\
        .order_by("lane_pos").distinct("lane_pos").count()
    frame_list = Record.objects.filter(road=road)\
        .order_by("frame_id").distinct("frame_id").values_list("frame_id", flat=True)
    first_frame = frame_list.first()
    # 选择一个初始的sampler
    sampler = Vehicle.objects.filter(record__frame_id=first_frame)[0]

    if sampler is None:
        print "无法找到初始的sampler"
        return
    print frame_list.count()
    for frame in frame_list:
        sampler = estimate(sampler, frame, road, lane_num)


if __name__ == "__main__":
    main()
