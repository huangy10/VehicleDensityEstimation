import sys
import os

from mobsampling_result_handle import mean_relative_error

from django.core.wsgi import get_wsgi_application
from django.db.models import F

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

from simulator.models import SimulationRecord
from VehicleDataORM.models import Vehicle, Record, Road

def main():
    data = SimulationRecord.objects.filter(estimation_method="runner_2", loss_rate__range=(0.49, 0.51))
    print data.count()
    road = Road.objects.all()[0]
    i = 0
    for d in data:
        if abs(d.estimate_value - d.real_value) / d.real_value > 1:
            print d.estimate_value, d.real_value, d.frame_id, d.lane_pos,
            print Record.objects.filter(road=road, frame_id=d.frame_id, lane_pos=d.lane_pos, spacing_m__gt=1)\
                .values_list("spacing_m", flat=True)
            i += 1
    print "================"
    print i
    # print data.count()
    print mean_relative_error(data)

    # data = SimulationRecord.objects.filter(estimation_method="runner_2", extra_params="threshold:29")
    # print data.count()
    # print mean_relative_error(data)

def main2():
    road = Road.objects.all().first()
    records = Record.objects.filter(road=road, frame_id=9466, lane_pos=3)
    for record in records:
        print record.local_y_m, record.spacing_m

if __name__ == "__main__":
    # print SimulationRecord.objects.all().distinct("estimation_method").values("estimation_method")
    main()
