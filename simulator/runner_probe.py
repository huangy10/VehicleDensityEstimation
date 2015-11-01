# coding=utf-8
import threading
import Queue
import time
import sys
import getopt
import os
import random

from django.core.wsgi import get_wsgi_application

sys.path.extend(['/Users/Lena/Project/Python/DataScience/VehicleDensityEstimation', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VehicleDensityEstimation.settings")
application = get_wsgi_application()


from VehicleDataORM.models import Road, Record
from simulator.models import SimulationRecord

__author__ = 'Woody Huang'
__version__ = '1.0.0'

data_queue = Queue.Queue()


class DataLoader(threading.Thread):

    def __init__(self, road, frame_num_per_fetch=5000, frame_skip=1000, manager=None,  *args, **kwargs):

        """
         :param frame_num_per_fetch 每次循环取出来的frame的数量
         :param frame_skip 跳过前面的部分frame
        """
        super(DataLoader, self).__init__()
        self.frame_num_per_fetch = frame_num_per_fetch
        self.min_frame_id = 0
        self.max_frame_id = 0
        self.frame_skip = frame_skip
        self.road = road
        self.manager = manager

    def start(self):
        print '====>DataLoader %s preparing' % self.name
        frame_ids = Record.objects.filter(road=self.road).order_by('frame_id')
        self.min_frame_id = frame_ids.first().frame_id
        self.max_frame_id = frame_ids.last().frame_id
        return super(DataLoader, self).start()

    def run(self):
        print '====>DataLoader %s starts' % self.name
        cur_frame = max(self.min_frame_id, self.frame_skip)
        while True:
            if cur_frame >= self.max_frame_id:
                break
            frames_to_fetch = min(self.frame_num_per_fetch, self.max_frame_id - cur_frame)
            print '====>DataLoader %s visiting database' % self.name
            records = Record.objects.filter(road=self.road, processed=False,
                                            frame_id__in=range(cur_frame, cur_frame + frames_to_fetch)) \
                .order_by('frame_id', 'local_y_m')

            print '====>DataLoader %s fetched %s frames' % (self.name, frames_to_fetch)
            if frames_to_fetch > 0:
                data_queue.put(list(records))
            cur_frame += frames_to_fetch

        print 'DataLoader %s Finished' % self.name
        self.manager.loading_finished = True


class Manager(threading.Thread):

    def __init__(self, worker_num=3, z=None, frame_per_fetch=5000, frame_skip=1000, method_name='method_name',
                 loss_rate=None, **kwargs):
        super(Manager, self).__init__()
        self.worker_num = worker_num
        self.loss_rate = loss_rate
        self.workers = []
        self.z = z
        self.road = Road.objects.all()[0]
        self.data_loader = DataLoader(self.road, frame_num_per_fetch=frame_per_fetch, frame_skip=frame_skip,
                                      manager=self)
        self.data_loader.name = "0"
        self.method_name = method_name
        self.reporter = Reporter(self)
        self.loading_finished = False

    def create_workers(self):
        for i in range(self.worker_num):
            worker = Worker(road=self.road, z=self.z, method_name=self.method_name, manager=self,
                            loss_rate=self.loss_rate)
            worker.name = str(i)
            self.workers.append(worker)

    def start(self):
        self.create_workers()
        for worker in self.workers:
            worker.start()
        self.data_loader.start()
        self.reporter.start()
        super(Manager, self).start()

    def run(self):
        worker_switch = 0
        while True:
            if data_queue.qsize() == 0 and self.loading_finished:
                for w in self.workers:
                    w.join()
                break
            records = data_queue.get()
            cur_frame = records[0].frame_id
            package = []
            for record in records:

                if record.frame_id == cur_frame:
                    package.append(record)
                else:
                    self.workers[worker_switch].working_queue.put(package)
                    cur_frame += 1
                    worker_switch = (worker_switch + 1) % self.worker_num
                    package = []

            data_queue.task_done()

        print '====>仿真主线程完成并退出'


class Reporter(threading.Thread):

    def __init__(self, manager):
        super(Reporter, self).__init__()
        self.manager = manager

    def run(self):
        while True:
            time.sleep(5)
            if self.manager.is_alive():
                for w in self.manager.workers:
                    print "====>Worker %s queue size is %s" % (w.name, w.working_queue.qsize())
            else:
                break


class Worker(threading.Thread):

    def __init__(self, z=[], road=None, method_name='probe_based_m', manager=None, loss_rate=[]):
        super(Worker, self).__init__()
        self.manager = manager
        self.working_queue = Queue.Queue()
        self.cur_queue_frames = set()
        self.cur_working_frame = -1
        try:
            self.z = map(lambda x: float(x), z)
        except TypeError:
            self.z = float(z)
        self.road = road
        self.method_name = method_name
        self.loss_rate=loss_rate

    def start(self):
        print '====>Worker %s starts' % self.name
        return super(Worker, self).start()

    def run(self):
        while True:
            if self.working_queue.qsize() == 0 and self.manager.loading_finished:
                break
            package = self.working_queue.get()
            self.estimator(package)
            self.working_queue.task_done()
        print '====>Worker %s finished' % self.name

    def estimator(self, data):
        if len(data) == 0:
            return
        # cur_frame = data[0].frame_id
        # print '====>Worker %s 开始处理第%s帧的数据, 数据包的长度为%s' % (self.name, cur_frame, len(data))

        def estimate_single_lane(data_single_lane, z, loss_rate):
            if len(data_single_lane) < 2:
                return -1
            probe = data_single_lane[0]
            probe_pos = probe.local_y_m
            k = 0
            for record in data_single_lane:
                if 0 < record.local_y_m - probe_pos <= z:
                    if random.random() >= loss_rate:
                        k += 1
            return k / z

        def data_re_organizer(raw_data, lane_num=4):
            place_holder = []
            for _ in range(lane_num):
                place_holder.append([])
            for record in raw_data:
                if record.lane_pos <= lane_num:
                    place_holder[record.lane_pos - 1].append(record)
            return place_holder

        data = data_re_organizer(data)

        for (lane_pos, a) in enumerate(data):
            for z in self.z:
                for l in self.loss_rate:
                    estimated_value = estimate_single_lane(a, z, l)
                    if estimated_value >= 0:
                        SimulationRecord.objects.create(
                            road=self.road,
                            frame_id=a[0].frame_id,
                            lane_pos=lane_pos+1,
                            estimate_value=estimated_value,
                            real_value=len(a)/self.road.road_length_m,
                            estimation_method=self.method_name,
                            loss_rate=l,
                            z=z
                        )


def parse_command_line_params():
    """ 这个函数从命令行参数中解析出仿真参数
     -w: worker的数量
     -z: 仿真的z参数
     -f: DataLoader每次从数据库中取出的帧数
     -m: 方法名称，注意以test开头的名称的仿真产生的结构数据会在仿真完成后删除
     -l: loss rate，丢包率
    """
    opt, args = getopt.getopt(sys.argv[1:], "w:z:f:m:l:")
    raw_param = dict()
    for op, value in opt:
        raw_param[op] = value
    param = dict()

    if '-z' in raw_param:
        z_str = raw_param['-z']
        if ':' in z_str:
            z_params = map(lambda x: int(x), z_str.split(':'))
            if len(z_params) == 2:
                param['z'] = range(z_params[0], z_params[1])
            else:
                param['z'] = range(z_params[0], z_params[1], z_params[2])
        else:
            param['z'] = [int(raw_param['-z']), ]
    else:
        param['z'] = [100, ]

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
    param['method_name'] = raw_param.get('-m', 'test')
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


