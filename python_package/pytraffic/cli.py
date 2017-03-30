import logging
import argparse
from pytraffic import config
from pytraffic.app import PyTraffic


def _configure_logging():
    """Configure logger."""
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


def _create_parser():
    """Configure argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--kafka',
                        help='Kafka bootstrap server address in format hostname:port')
    parser.add_argument('--bt_collector', action='store_true',
                        help='Start bluetooth collector')
    parser.add_argument('--counters_collector', action='store_true',
                        help='Start counters collector')
    parser.add_argument('--il_collector', action='store_true',
                        help='Start inductive loops collector')
    parser.add_argument('--pollution_collector', action='store_true',
                        help='Start pollution collector')
    parser.add_argument('--lpp_collector', nargs='*',
                        choices=['station', 'static', 'live'],
                        help='Start lpp collector')
    parser.add_argument('--plot', nargs='*', choices=['bt', 'counters', 'il'],
                        help='Plot map')
    parser.add_argument("--config", help="Configuration file to use",
                        default="local.conf")
    return parser


def main():
    """
    Override config with environment variables, configure logger and argument
    parser and start collectors.
    """
    log = _configure_logging()
    parser = _create_parser()
    args = parser.parse_args()
    conf_obj = config.Config()
    conf = conf_obj.load_from_file(args.config)

    py = PyTraffic(log, conf, args)
    py.run()