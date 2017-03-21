import logging
from pytraffic.settings import override
from pytraffic.pytraffic.pytraffic import PyTraffic


def _configure_logging():
    fmt_stream = logging.Formatter("[%(levelname)s] - %(message)s")
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(fmt_stream)
    handler_stream.setLevel(logging.INFO)

    fmt_file = logging.Formatter(
        "%(asctime)s %(name)s:%(lineno)s [%(levelname)s] - %(message)s"
    )
    handler_file = logging.FileHandler(".pytraffic.log")
    handler_file.setFormatter(fmt_file)
    handler_file.setLevel(logging.DEBUG)

    log = logging.getLogger("pytraffic")
    log.addHandler(handler_stream)
    log.addHandler(handler_file)
    log.setLevel(logging.DEBUG)

    return log


def main():
    override()
    log = _configure_logging()

    pt = PyTraffic(log)
    pt.run()
