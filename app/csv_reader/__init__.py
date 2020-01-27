from .providers import Ros, Ss

def csv_reader_factory(csv):
    if csv == "ro":
        return Ros()
    if csv == "sp":
        return Ss()
