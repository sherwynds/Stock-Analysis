import abc
import os

import constants as C


class Instrument(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, start_date, end_date):
        self.path = None
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    @abc.abstractmethod
    def download_data(self):
        pass

    @abc.abstractmethod
    def get_path(self):
        return self.path

    @abc.abstractmethod
    def is_saved(self):
        return os.path.exists(self.get_path())

