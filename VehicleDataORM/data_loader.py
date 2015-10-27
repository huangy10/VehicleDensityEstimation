# !coding=utf-8
import os
import xlrd
import sys
import thread
import time

from django.conf import settings
from django.core.wsgi import get_wsgi_application

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()

from VehicleDataORM.models import Road, Vehicle, Record

__author__ = 'Woody Huang'
__version__ = '1.0.0'

start_processing = False
total_num = 0
processed_num = 0

def load_from_excel_to_database(filename, description_file=None, book=None):
    """
    """
    global total_num, start_processing, processed_num
    if book is None:
        print '开始尝试打开文件:%s \n' % filename
        book = xlrd.open_workbook(filename)
        print '成功打开文件:%s \n' % filename
    start_processing = True
    sheets = book.sheets()
    road, _ = Road.objects.get_or_create(name=filename, description=filename)
    new_record = 0
    for sheet in sheets:
        print 'Go to next sheet'
        n_rows = sheet.nrows
        total_num += n_rows
        # print 'File %s has %s rows in total' % (filename, n_rows)
        for r in range(n_rows):
            data = sheet.row_values(r)
            vehicle, created = Vehicle.objects.get_or_create(v_id=int(data[0]), road=road)
            if created:
                vehicle.width = data[9]
                vehicle.length = data[8]
                vehicle.name = str(data[0])
                vehicle.vehicle_class = int(data[10])
            preceding, _ = Vehicle.objects.get_or_create(v_id=int(data[14]), road=road)
            following, _ = Vehicle.objects.get_or_create(v_id=int(data[15]), road=road)
            Record.objects.get_or_create(description_file=description_file,
                                         vehicle=vehicle,
                                         road=road,
                                         frame_id=int(data[1]),
                                         global_time=long(data[3]),
                                         local_x=data[4],
                                         local_y=data[5],
                                         global_x=data[6],
                                         global_y=data[7],
                                         velocity=data[11],
                                         acceleration=data[12],
                                         lane_pos=int(data[13]),
                                         preceding_vehicle=preceding,
                                         following_vehicle=following,
                                         spacing=data[16],
                                         headway=data[17])
            processed_num += 1
        new_record += n_rows
    return new_record


def load_from_text_to_database(filename, callback):
    return callback()


def main():
    path = 'VehicleDataORM/data/'

    files = ['0750am-0805am.xlsx', '0805am-0820am.xlsx', '0820am-0835am.xlsx']

    def load(filename):
        ext = filename.split('.')[-1]
        if ext in ['xlsx', 'xls']:
            count = load_from_excel_to_database(filename)
            # count = load_from_excel_to_database(filename)
        elif ext == 'txt':
            count = load_from_text_to_database(filename)
        else:
            print 'Format not supported'
        return count

    def reporter():
        print 'Reporter 启动'
        global processed_num
        while True:
            time.sleep(10)
            if start_processing:
                print "-->已经处理了%s/%s" % (processed_num, total_num)
            else:
                print "loading"
    thread.start_new_thread(reporter, ())
    for f in files:
        load(path + f)
    print "=======================Finished========================"


if __name__ == '__main__':
    main()
