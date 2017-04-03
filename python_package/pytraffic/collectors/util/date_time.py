import datetime, pytz

"""
Here are some useful functions for working with time.
"""


def now_isoformat():
    """
    Returns:
        str: Current time in iso format.
    """
    return datetime.datetime.utcnow().replace(second=0,
                                              microsecond=0).isoformat() + 'Z'


def today_timestamp():
    """
    Returns:
         str: Timestamp of today at midnight.
    """
    date = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0,
                                              microsecond=0, tzinfo=pytz.utc)
    return str(round(date.timestamp() * 1000))


def hour_minut_to_utc(hour, minute):
    """
    This function crates a datatime object with the given hour and minute. It
    then changes it to utc and returns a iso formatted datetime.

    Args:
        hour (int): Given hour.
        minute (int): Given minutes.

    Returns:
        str: Utc time in iso format.
    """
    local = pytz.timezone("Europe/Ljubljana")
    naive = datetime.datetime.now().replace(hour=hour, minute=minute, second=0,
                                            microsecond=0)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def local_to_utc(local_time):
    """
    This function returns utc time of the given local time in iso format.

    Args:
        local_time (str): Local time.

    Returns:
        str: Utc time in iso format.
    """
    local = pytz.timezone("Europe/Ljubljana")
    naive = datetime.datetime.strptime(local_time, "%Y-%m-%dT%H:%M:%S.000Z")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def isoformat_to_utc(iso_time):
    """
    This function returns utc time of the given iso formatted time.

    Args:
        iso_time (str): Given time.

    Returns:
        str: Utc time in iso format.
    """
    dt = datetime.datetime.strptime(''.join(iso_time.rsplit(':', 1)),
                                          '%Y-%m-%dT%H:%M:%S%z')
    utc_dt = dt.astimezone(pytz.utc)

    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
