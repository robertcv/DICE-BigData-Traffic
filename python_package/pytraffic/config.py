import json
import copy
import collections

CONF = {
    # Apache Kafka config
    'kafka_host': 'host',
    # Bluetooth sensors
    'bt_sensors': {
        'last_url': 'https://datacloud-timon.xlab.si/data_access/bt_sensors/velocities_avgs_last/',
        'sensors_url': 'https://datacloud-timon.xlab.si/data_access/bt_sensors/sensors/',
        'timon_username': 'username',
        'timon_password': 'password',
        'timon_crt_file': 'crt',
        'img_dir': None,
        'data_file': 'data/bt_sensors.json',
        'data_age': 60 * 60 * 24,  # 1 day
        'not_lj': ['BTR0219', 'BTR0218', 'BTR0217', 'BTR0213'],
        'kafka_topic': 'bt_json'
    },
    # Traffic counters
    'counters': {
        'url': 'https://opendata.si/promet/counters/',
        'img_dir': None,
        'kafka_topic': 'counter_json'
    },
    # Inductive loops
    'inductive_loops': {
        'es_host': '10.30.1.132',
        'es_port': 9200,
        'es_index': 'inductive_loops',
        'img_dir': None,
        'kafka_topic': 'inductive_json'
    },
    # LPP traffic
    'lpp': {
        'station': {
            'url': 'http://194.33.12.24/stations/getAllStations',
            'kafka_topic': 'lpp_station_json',
            'data_file': 'data/stations.json',
            'direction_file': 'data/stations_directions.csv'
        },
        'routes_on_station': {
            'url': 'http://194.33.12.24/stations/getRoutesOnStation',
            'data_file': 'data/routes_on_station.json'
        },
        'static': {
            'url': 'http://194.33.12.24/timetables/getArrivalsOnStation',
            'kafka_topic': 'lpp_static_json'
        },
        'live': {
            'url': 'http://194.33.12.24/timetables/liveBusArrival',
            'kafka_topic': 'lpp_live_json'
        },
        'route': {
            'groups_url': 'http://194.33.12.24/routes/getRouteGroups',
            'url': 'http://194.33.12.24/routes/getRoutes',
            'data_file': 'data/routes.json'
        },
        'data_age': 60 * 60 * 24  # 1 day
    },
    # Air pollution
    'pollution': {
        'url': 'http://www.ljubljana.si/si/zivljenje-v-ljubljani/okolje-prostor-bivanje/stanje-okolja/zrak/',
        'kafka_topic': 'pollution_json'
    },
    # Ljubljana loaction
    'location': {
        'min_lng': 14.44,
        'max_lng': 14.58,
        'min_lat': 46.0,
        'max_lat': 46.1
    },
    # Web scraper
    'scraper': {
        'timeout': 0.5,
        'retries': 10,
        'sleep': 2,
        'ignore_status_code': False
    }
}


class Config(object):
    def __init__(self):
        self.conf = copy.deepcopy(CONF)

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.conf, f)

    def load_from_file(self, path):
        with open(path) as f:
            data = json.load(f)
        self.conf = self.update(self.conf, data)
        return self.conf

    def update(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = self.update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        return d