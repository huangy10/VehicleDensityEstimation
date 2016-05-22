# coding=utf-8
import os
import sys
from django.core.wsgi import get_wsgi_application
import random
import math

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()


from VehicleDataORM.models import Road, Record
from simulator.models import SimulationRecord


COMMUNICATION_RANGE = 100


def estimate_with_loss(frame, road, lane_pos, loss_rate=0.5):
    records = Record.objects.filter(road=road, frame_id=frame, lane_pos=lane_pos).order_by("local_y_m")
    real_value = records.count() / road.road_length_m
    if real_value == 0:
        return
    if records.count() < 2:
        SimulationRecord.objects.create(
            road=road,
            frame_id=frame,
            lane_pos=lane_pos,
            estimate_value=0,
            real_value=real_value,
            loss_rate=loss_rate,
            z=COMMUNICATION_RANGE,
            estimation_method="exploiting..."
        )
        return
    prob = records[0]
    prob_pos = prob.local_y_m
    last_pos = prob_pos
    i = 0
    root_point = prob_pos
    for record in records[1:]:
        # 从prob往后搜索下一个节点
        if record.local_y_m - root_point < COMMUNICATION_RANGE:
            if random.random() >= loss_rate:
                i += 1
            else:
                continue
        else:
            # 搜索中断,跳转到新的root节点
            if root_point == last_pos:
                break
            root_point = last_pos
            if record.local_y_m - root_point < COMMUNICATION_RANGE:
                i += 1
            else:
                break

        last_pos = record.local_y_m

    SimulationRecord.objects.create(
        road=road,
        frame_id=frame,
        lane_pos=lane_pos,
        estimate_value=math.log(i+1)/COMMUNICATION_RANGE,
        real_value=real_value,
        loss_rate=loss_rate,
        z=COMMUNICATION_RANGE,
        estimation_method="exploiting..."
    )
    return i


def main():
    print "=================Simulation Start===================="
    SimulationRecord.objects.filter(estimation_method="exploiting...").delete()
    road = Road.objects.all()[0]
    # lanes = Record.objects.filter(road=road)\
    #     .order_by("lane_pos").distinct("lane_pos").values_list("lane_pos", flat=True)
    lanes = range(1, 5)
    frame_list = Record.objects.filter(road=road)\
        .order_by("frame_id").distinct("frame_id").values_list("frame_id", flat=True)
    for frame in frame_list:
        for lane in lanes:
            print frame, lane
            for l in [0, 0.05, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
                estimate_with_loss(frame, road, lane, l)


if __name__ == '__main__':
    main()
