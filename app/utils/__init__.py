from time import mktime
from datetime import datetime

def datetime_to_timestamp(dt):
    if isinstance(dt, datetime):
        return mktime(dt.timetuple())
    else:
        raise AttributeError("datetime_to_timestamp : args 1 must be a datetime")
