from time import mktime
from datetime import datetime

def datetime_to_timestamp(dt):
    if isinstance(dt, datetime):
        return mktime(dt.timetuple())
    else:
        raise AttributeError("datetime_to_timestamp : args 1 must be a datetime")


def value_or_zero(value):
    '''
    :return: 0 if value like nullabletype or value
    '''
    if not value or (isinstance(value, str) and value.lower() == 'null'):
        return 0
    else:
        return value
