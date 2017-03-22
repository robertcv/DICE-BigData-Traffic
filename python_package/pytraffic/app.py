from . import settings
from .collectors.bt_sensors import BtSensors
from .collectors.counters import TrafficCounter
from .collectors.inductive_loops import InductiveLoops
from .collectors.lpp import LppTraffic
from .collectors.pollution import AirPollution


class PyTraffic:
    def __init__(self, logger, args):
        self.logger = logger
        self.args = args

        if self.args.kafka:
            settings.KAFKA_HOST, settings.KAFKA_PORT = self.args.kafka.split(':')

        self.bs = None
        self.tc = None
        self.il = None
        self.ap = None
        self.lt = None

        if self.args.bt_collector: self.bt_sensors()
        if self.args.counters_collector: self.counters()
        if self.args.il_collector: self.inductive_loops()
        if self.args.pollution_collector: self.pollution()
        if self.args.lpp_collector: self.lpp(self.args.lpp_collector)
        if self.args.plot: self.plot(self.args.plot)

    def bt_sensors(self):
        self.logger.info('Start initializing bluetooth sensors collector.')
        self.bs = BtSensors()
        self.logger.info('Finished initializing bluetooth sensors collector.')
        self.logger.info('Start sending bluetooth sensors data to Kafka.')
        self.bs.run()
        self.logger.info('Finished sending bluetooth sensors data to Kafka.')

    def counters(self):
        self.logger.info('Start initializing traffic counter collector.')
        self.tc = TrafficCounter()
        self.logger.info('Finished initializing traffic counter collector.')
        self.logger.info('Start sending traffic counters data to Kafka.')
        self.tc.run()
        self.logger.info('Finished sending traffic counters data to Kafka.')

    def inductive_loops(self):
        self.logger.info('Start initializing inductive loops collector.')
        self.il = InductiveLoops()
        self.logger.info('Finished initializing inductive loops collector.')
        self.logger.info('Start sending inductive loops data to Kafka.')
        self.il.run()
        self.logger.info('Finished sending inductive loops data to Kafka.')

    def pollution(self):
        self.logger.info('Start initializing air pollution collector.')
        self.ap = AirPollution()
        self.logger.info('Finished initializing air pollution collector.')
        self.logger.info('Start sending air pollution data to Kafka.')
        self.ap.run()
        self.logger.info('Finished sending air pollution data to Kafka.')

    def lpp(self, args):
        self.logger.info('Start initializing lpp collector.')
        self.lt = LppTraffic()
        self.logger.info('Finished initializing lpp collector.')
        if 'station' in args:
            self.logger.info('Start sending lpp station data to Kafka.')
            self.lt.run_station()
            self.logger.info('Finished sending lpp station data to Kafka.')
        if 'static' in args:
            self.logger.info('Start sending lpp static data to Kafka.')
            self.lt.run_static()
            self.logger.info('Finished sending lpp static data to Kafka.')
        if 'live' in args:
            self.logger.info('Start sending lpp live data to Kafka.')
            self.lt.run_live()
            self.logger.info('Finished sending lpp live data to Kafka.')


    def plot(self, args):

        if 'bt' in args:
            if self.bs is None:
                self.logger.info('Start initializing bluetooth sensors collector.')
                self.bs = BtSensors()
                self.logger.info('Finished initializing bluetooth sensors collector.')
            self.logger.info('Start crating bluetooth sensors map.')
            self.bs.plot_map('BT v Ljubljani', (18, 18), 400, 14, 5, (0.001, 0.0005), 10, 'bt_lj.png')
            self.logger.info('Finished crating bluetooth sensors map.')

        if 'counters' in args:
            if self.tc is None:
                self.logger.info('Start initializing traffic counter collector.')
                self.tc = TrafficCounter()
                self.logger.info('Finished initializing traffic counter collector.')
            self.logger.info('Start crating traffic counters map.')
            self.tc.plot_map('Stevci', (20, 20), 500, 14, 8, "counters.png")
            self.logger.info('Finished crating traffic counters map.')

        if 'il' in args:
            if self.il is None:
                self.logger.info('Start initializing inductive loops collector.')
                self.il = InductiveLoops()
                self.logger.info('Finished initializing inductive loops collector.')
            self.logger.info('Start crating inductive loops map.')
            self.il.plot_map('Inductive loops', (20, 20), 500, 14, 5, (0.0005, 0.00025), 20, 'inductive.png')
            self.logger.info('Finished crating inductive loops map.')