import abc
import datetime as dt
import os
from functools import wraps


class Timerange(object):
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def get_name(self):
        return self.name

    def get_time_range(self):
        start = self.convert_time_to_int(self.start)
        end = self.convert_time_to_int(self.end)
        return (start, end)

    def convert_time_to_int(self, timestamp):
        mtime = 0
        time = timestamp.split(" ")[0].strip()
        mtime = \
            int(dt.datetime.strftime(dt.datetime.strptime(time, "%H:%M"),
                "%H%M"))
        if timestamp.find("PM") != -1 and not timestamp.startswith("12"):
            mtime += 1200
        return mtime

    def update_time_range(self, start, end):
        self.start = start
        self.end = end


class CSVReader(metaclass=abc.ABCMeta):
    """Base Reader class"""
    csv_path, res = None, []

    def _validation(func):
        @wraps(func):
        def wrapped(obj, *args, **kwargs):
            getattr(obj, '_validate_' + func.__name__)(*args)
            return func(obj, *args, **kwargs)
        return wrapped


    def readCSV(self):
        """Implement csv reader"""
        pass


    def reformat_data(self, *args):
        """Tuning dataset"""
        pass


    @_validation
    def update_range(self, *args):
        pass


    @_validation
    def set_csvpath(self, path):
        self.csv_path = path
        return self


    def _validate_set_csvpath(self, *args):
        csvpath = args[0]
        if csvpath is None or not isinstance(csvpath, str):
            raise ValueError
        if not os.path.exists(csvpath):
            raise ValueError


class Ros(CSVReader):
    def readCSV(self):
        with open(self.csv_path) as rt:
            # Assume 1st line is header
            line = rt.readline()
            while line:
                line = rt.readline()
                if line.strip():
                    name, start, end = self.reformat_data(line.strip())
                    timerange = Timerange(name, start, end)
                    self.res.append(timerange)


    def reformat_data(self, line):
        start = line.split(",")[0].split('"')[1].strip()
        end = line.split(",")[1].split('"')[1].strip()
        name = line.split(",")[-1].split('"')[1].strip()
        return name, start, end


    def get_rotation_range(self, name):
        for elem in self.res:
            if isinstance(elem, Timerange) and elem.name == name:
                return elem.get_time_range()
        return


    def get_rotation_names(self):
        return [e.name for e in self.res if isinstance(e, Timerange)]


    def update_range(self, name, start, end):
        for elem in self.res:
            if isinstance(elem, Timerange) and elem.name == name:
                elem.update_time_range(start, end)
                return elem
        return


    def add_rotation(self, name, start, end):
        timerange = Timerange(name, start, end)
        self.res.append(timerange)
        return self.get_rotation_names()


class Ss(CSVReader):
    def readCSV(self):
        with open(self.csv_path) as dl:
            line = dl.readline()
            while line:
                line = dl.readline()
                if line.strip():
                    creative, date, rts, spend, view =\
                        self.reformat_data(line.strip())
                    meta = MetaData(date, rts, spend, view)
                    self.res.append([creative, meta])


    def _convert_time_to_int(self, timestamp):
        mtime = 0
        time = timestamp.split(" ")[0].strip()
        mtime = \
            int(dt.datetime.strftime(dt.datetime.strptime(time, "%H:%M"),
                "%H%M"))
        if timestamp.find("PM") != -1:
            mtime += 1200
        return mtime


    def reformat_data(self, line):
        # TODO: use regex might be better
        date = line.split(",")[0].split('"')[1].strip()
        time = line.split(",")[1].split('"')[1].strip()
        timenum = self._convert_time_to_int(time)
        rotations = self._get_ro(timenum)
        creative = line.split(",")[2].strip().split('"')[1]
        spend = line.split(",")[3].strip()
        view = line.split(",")[-1].strip()
        return creative, date, rotations, float(spend), int(view)


def _get_ro(self, time):
    rts = []
    for rtname in self.rt.get_rotation_names():
        start, end = self.rt.get_rotation_range(rtname)
        if time > start and time < end:
            rts.append(rtname)
    return rts
