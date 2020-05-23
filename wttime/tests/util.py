from datetime import datetime
import dateutil.tz as tz


def utc_midnight(y, m, d):
    return datetime(y, m, d, tzinfo=tz.tzutc())
