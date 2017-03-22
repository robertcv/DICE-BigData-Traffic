import logging, argparse
from .settings import override
from .app import PyTraffic


def _configure_logging():
    fmt_stream = logging.Formatter("[%(levelname)s] - %(message)s")
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(fmt_stream)
    handler_stream.setLevel(logging.INFO)

    fmt_file = logging.Formatter(
        "%(asctime)s %(name)s:%(lineno)s [%(levelname)s] - %(message)s"
    )
    handler_file = logging.FileHandler(".cli_tool.log")
    handler_file.setFormatter(fmt_file)
    handler_file.setLevel(logging.DEBUG)

    log = logging.getLogger("cli_tool")
    log.addHandler(handler_stream)
    log.addHandler(handler_file)
    log.setLevel(logging.DEBUG)

    return log


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kafka', help='Kafka bootstrap server address in format hostname:port')
    parser.add_argument('--bt_collector', action='store_true', help='Start bluetooth collector')
    parser.add_argument('--counters_collector', action='store_true', help='Start counters collector')
    parser.add_argument('--il_collector', action='store_true', help='Start inductive loops collector')
    parser.add_argument('--pollution_collector', action='store_true', help='Start pollution collector')
    parser.add_argument('--lpp_collector', nargs='*', choices=['station', 'static', 'live'], help='Start lpp collector')
    parser.add_argument('--plot', nargs='*', choices=['bt', 'counters', 'il'], help='Plot map')
    return parser

def main():
    override()
    log = _configure_logging()
    parser = _create_parser()
    args = parser.parse_args()

    PyTraffic(log, args)