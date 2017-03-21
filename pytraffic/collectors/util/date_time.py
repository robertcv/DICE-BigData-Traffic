import datetime, pytz


def now_isoformat():
    return datetime.datetime.now().isoformat()


def today_timestamp():
    date = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    return str(round(date.timestamp() * 1000))
