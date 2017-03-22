import datetime, pytz

"""
Here are some useful functions for working with time.
"""


def now_isoformat():
    """
    Returns:
        str: Current time in iso format.
    """
    return datetime.datetime.now().isoformat()


def today_timestamp():
    """
    Returns:
         str: Timestamp of today at midnight.
    """
    date = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    return str(round(date.timestamp() * 1000))
