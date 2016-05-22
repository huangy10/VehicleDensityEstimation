import os
import yaml


class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = GlobalConfigure()
        return cls._instance


class GlobalConfigure(object):

    _data = yaml.load(open(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'settings.yaml')))

    def get_threshold(self):
        return self._data["threshold"]

    def get_normal_percentages(self):
        return self._data['normal_percentage']

    def get_lmda(self):
        return float(self._data['lmda'])

    def get_phi_0(self):
        return float(self._data['attack'][0])

    def get_phi_1(self):
        return float(self._data['attack'][1])
