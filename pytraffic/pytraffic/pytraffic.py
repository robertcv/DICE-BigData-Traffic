from pytraffic.collectors.bt_sensors.bt_sensors import BtSensors
from pytraffic.collectors.counters.counters import TrafficCounter
from pytraffic.collectors.inductive_loops.inductive_loops import InductiveLoops
from pytraffic.collectors.lpp.lpp import LppTraffic
from pytraffic.collectors.pollution.pollution import AirPollution


class PyTraffic:
    def __init__(self, logger):
        self.logger = logger

        self.logger.info('Start initializing bluetooth sensors collector.')
        self.bs = BtSensors()
        self.logger.info('Finished initializing bluetooth sensors collector.')

        self.logger.info('Start initializing traffic counter collector.')
        self.tc = TrafficCounter()
        self.logger.info('Finished initializing traffic counter collector.')

        self.logger.info('Start initializing inductive loops collector.')
        self.il = InductiveLoops()
        self.logger.info('Finished initializing inductive loops collector.')

        self.logger.info('Start initializing lpp collector.')
        self.lt = LppTraffic()
        self.logger.info('Finished initializing lpp collector.')

        self.logger.info('Start initializing air pollution collector.')
        self.ap = AirPollution()
        self.logger.info('Finished initializing air pollution collector.')

    def run(self):
        self.logger.info('Start sending bluetooth sensors data to Kafka.')
        self.bs.run()
        self.logger.info('Finished sending bluetooth sensors data to Kafka.')

        self.logger.info('Start sending traffic counters data to Kafka.')
        self.tc.run()
        self.logger.info('Finished sending traffic counters data to Kafka.')

        self.logger.info('Start sending inductive loops data to Kafka.')
        self.il.run()
        self.logger.info('Finished sending inductive loops data to Kafka.')

        self.logger.info('Start sending lpp station data to Kafka.')
        self.lt.run_station()
        self.logger.info('Finished sending lpp station data to Kafka.')

        self.logger.info('Start sending lpp static data to Kafka.')
        self.lt.run_static()
        self.logger.info('Finished sending lpp static data to Kafka.')

        self.logger.info('Start sending lpp live data to Kafka.')
        self.lt.run_live()
        self.logger.info('Finished sending lpp live data to Kafka.')

        self.logger.info('Start sending air pollution data to Kafka.')
        self.ap.run()
        self.logger.info('Finished sending air pollution data to Kafka.')

    def plot(self):
        self.logger.info('Start crating bluetooth sensors map.')
        self.bs.plot_map('BT v Ljubljani', (18, 18), 400, 14, 5, (0.001, 0.0005), 10, 'bt_lj.png')
        self.logger.info('Finished crating bluetooth sensors map.')

        self.logger.info('Start crating traffic counters map.')
        self.tc.plot_map('Stevci', (20, 20), 500, 14, 8, "counters.png")
        self.logger.info('Finished crating traffic counters map.')

        self.logger.info('Start crating inductive loops map.')
        self.il.plot_map('Inductive loops', (20, 20), 500, 14, 5, (0.0005, 0.00025), 20, 'inductive.png')
        self.logger.info('Finished crating inductive loops map.')