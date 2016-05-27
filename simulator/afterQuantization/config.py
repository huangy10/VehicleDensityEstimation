import os
import yaml


class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class GlobalConfigure(object):

    __metaclass__ = Singleton

    _data = yaml.load(open(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'settings.yaml')))

    def __init__(self):
        self.lmda = 0
        super(GlobalConfigure, self).__init__()

    def get_threshold(self):
        return self._data["threshold"]

    def get_normal_percentages(self):
        return self._data['normal_percentage']

    def get_lmda(self):
        if self.lmda == 0:
            return float(self._data['lmda'])
        return self.lmda

    def get_phi_0(self):
        return float(self._data['attack'][0])

    def get_phi_1(self):
        return float(self._data['attack'][1])
