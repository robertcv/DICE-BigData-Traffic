from pytraffic.collectors.bt_sensors.bt_sensors import BtSensors
from pytraffic.collectors.counters.counters import TrafficCounter
from pytraffic.collectors.inductive_loops.inductive_loops import InductiveLoops
from pytraffic.collectors.lpp.lpp import LppTraffic
from pytraffic.collectors.pollution.pollution import AirPollution


class PyTraffic:
    def __init__(self, logger):
        self.logger = logger
        self.bs = BtSensors()
        self.tc = TrafficCounter()
        self.il = InductiveLoops()
        self.lt = LppTraffic()
        self.ap = AirPollution()

    def run(self):
        self.bs.run()
        self.tc.run()
        self.il.run()
        self.lt.run_station()
        self.lt.run_static()
        self.lt.run_live()
        self.ap.run()

    def plot(self):
        self.bs.plot_map('BT v Ljubljani', (18, 18), 400, 14, 5, (0.001, 0.0005), 10, 'bt_lj.png')
        self.tc.plot_map('Stevci', (20, 20), 500, 14, 8, "counters.png")
        self.il.plot_map('Inductive loops', (20, 20), 500, 14, 5, (0.0005, 0.00025), 20, 'inductive.png')
