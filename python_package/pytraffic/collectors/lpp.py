import json
import csv

from .util import kafka_producer, scraper, files, date_time


class LppTraffic:
    """
    This combines everything lpp related. On init it loads stations and
    routes data or fetches it from web if it’s older the one day. One can
    then use run_station, run_static or run_live method to send data to Kafka.
    """

    def __init__(self, conf):
        """
        Initialize Kafka producers and web scrapers classes. Also load station
        and routes data.

        Args:
            conf (dict): This dict contains all configurations.

        """
        self.conf = conf['lpp'] # global lpp settings
        self.conf_lj = conf['location'] # lng and lat boundaries of Ljubljana
        self.conf_s = conf['scraper'].copy() # scraper settings
        self.conf_s['timeout'] = 1
        self.conf_si = self.conf_s.copy() # settings for ignoring status code
        self.conf_si['ignore_status_code'] = True
        self.w_scraper = scraper.Scraper(self.conf_s)
        # Some combinations of route - station do not have arrival time data
        # which means that we get a response code different form 200. When this
        # happens we do not wont to interrupt the program because this is not
        # really an error. The solution is to create a web scraper that ignores
        # status code errors.
        self.w_scraper_ignore = scraper.Scraper(self.conf_si)
        self.day = date_time.today_timestamp()
        self.live_producer = kafka_producer.Producer(
            conf['kafka_host'],
            self.conf['live']['kafka_topic'])
        self.station_producer = kafka_producer.Producer(
            conf['kafka_host'],
            self.conf['station']['kafka_topic'])
        self.static_producer = kafka_producer.Producer(
            conf['kafka_host'],
            self.conf['static']['kafka_topic'])
        self.stations_data_file = files.file_path(
            __file__,
            self.conf['station']['data_file'])
        self.stations_data = None
        self.routes_data_file = files.file_path(
            __file__,
            self.conf['route']['data_file'])
        self.routes_data = None
        self.routes_on_stations_data_file = files.file_path(
            __file__,
            self.conf['routes_on_station']['data_file'])
        self.routes_on_stations_data = []
        self.load_routes_on_stations_data()

    def get_local_data(self, file):
        """
        This loads a copy of data from local file.

        Args:
            file (str): Data file location.

        Returns:
            dict: Dictionary of data loaded form the file.

        """
        with open(file) as data_file:
            return json.load(data_file)

    def get_web_stations_data(self):
        """
        This requests station data from source url and combines it with local
        data about station direction. Then it checks if the station is located
        inside given area. Last it saves the data to a local file.
        """
        ijs_station_data = self.w_scraper.get_json(self.conf['station']['url'])

        data = dict()

        direction_file = files.file_path(__file__,
                                         self.conf['station']['direction_file'])

        with open(direction_file) as data_file:
            direction_data = list(csv.reader(data_file))

        direction_data_dict = dict()
        for station in direction_data:
            tmp = {
                'station_name': station[1],
                'station_direction': station[2],
            }
            direction_data_dict[station[0]] = tmp

        for station in ijs_station_data['data']:
            if station['ref_id'] in direction_data_dict and \
                self.conf_lj['min_lat'] < station['geometry']['coordinates'][1] < self.conf_lj['max_lat'] and \
                self.conf_lj['min_lng'] < station['geometry']['coordinates'][0] < self.conf_lj['max_lng']:

                tmp = {
                    'station_int_id': station['int_id'],
                    'station_ref_id': station['ref_id'],
                    'station_lng': station['geometry']['coordinates'][0],
                    'station_lat': station['geometry']['coordinates'][1],
                    'station_name': station['name'],
                    'scraped': date_time.now_isoformat()
                }

                tmp.update(direction_data_dict[station['ref_id']])
                data[str(station['int_id'])] = tmp

        with open(self.stations_data_file, 'w') as outfile:
            json.dump(data, outfile)
            self.stations_data = data

    def get_web_routes_data(self):
        """
        This requests route data from source url. It then processes the route
        name to get only the routes which drive regularly. Last it saves the
        data to a local file.
        """
        ijs_group_data = self.w_scraper.get_json(
            self.conf['route']['groups_url'])

        data = dict()
        for group in ijs_group_data['data']:
            if group['name'].isnumeric() and int(group['name']) <= 27:

                ijs_route_data = self.w_scraper_ignore.get_json(
                    self.conf['route']['url'] + '?route_id=' + group['id'])

                if ijs_route_data is None:
                    continue

                for route in ijs_route_data['data']:
                    tmp = {
                        'route_num': int(group['name']),
                        'route_int_id': route['int_id'],
                        'scraped': date_time.now_isoformat()
                    }
                    name = route['name']
                    if ';' in name and 'osnovna' in name:
                        name = name[:name.find(';')]
                    elif ';' in name:
                        continue

                    if name[1] == ' ':
                        tmp['route_num_sub'] = name[0]
                        name = name[2:]
                    else:
                        tmp['route_num_sub'] = ''

                    tmp['route_name'] = name
                    data[str(route['int_id'])] = tmp

        with open(self.routes_data_file, 'w') as outfile:
            json.dump(data, outfile)
            self.routes_data = data

    def load_stations_data(self):
        """
        First We check if we have a not to old local copy of stations data. If
        yes we load it from local file, if not we get the data from souse url
        and then create a local copy.
        """
        if files.old_or_not_exists(self.stations_data_file,
                                   self.conf['data_age']):
            self.get_web_stations_data()
        else:
            self.stations_data = self.get_local_data(self.stations_data_file)

    def load_routes_data(self):
        """
        First We check if we have a not to old local copy of routes data. If yes
        we load it from local file, if not we get the data from souse url and
        then create a local copy.
        """
        if files.old_or_not_exists(self.routes_data_file,
                                   self.conf['data_age']):
            self.get_web_routes_data()
        else:
            self.routes_data = self.get_local_data(self.routes_data_file)

    def get_web_routes_on_stations_data(self):
        """
        This requests route for all stations. Then we combine station and route
        into on entry. Last we saves the data to a local file.
        """
        data = []
        for station_int_id in self.stations_data:

            ijs_station_data = self.w_scraper_ignore.get_json(
                self.conf['routes_on_station']['url'] +
                '?station_int_id=' + station_int_id)

            for route in ijs_station_data['data']:
                route_int_id = str(route['route_int_id'])

                if 'name' in route and route_int_id in self.routes_data:
                    tmp = self.stations_data[station_int_id].copy()
                    tmp.update(self.routes_data[route_int_id])
                    tmp['scraped'] = date_time.now_isoformat()
                    data.append(tmp)

        with open(self.routes_on_stations_data_file, 'w') as outfile:
            json.dump({'data': data}, outfile)
            self.routes_on_stations_data = data

    def load_routes_on_stations_data(self):
        """
        First We load station and routes data. Then we check if we have a not to
        old local copy of routes on station data. If yes we load it from local
        file, if not we get the data from souse url and then create a local
        copy.
        """
        self.load_stations_data()
        self.load_routes_data()

        if files.old_or_not_exists(self.routes_on_stations_data_file,
                                   self.conf['data_age']):
            self.get_web_routes_on_stations_data()
        else:
            self.routes_on_stations_data = \
                self.get_local_data(self.routes_on_stations_data_file)['data']

    def run_live(self):
        """
        This scraps data for every station. It then checks if the bus arrival
        time (eta) is 0. This means that the buss is now on the station so we
        send its data the Kafka.
        """
        for station_int_id in self.stations_data:

            data = self.w_scraper.get_json(
                self.conf['live']['url'] + '?station_int_id=' + station_int_id)

            for route in data['data']:
                if route['eta'] == 0:
                    tmp = {
                        'station_int_id': int(station_int_id),
                        'route_int_id': route['route_int_id'],
                        'arrival_time': route['local_timestamp']
                    }
                    self.live_producer.send(tmp)
            self.live_producer.flush()

    def run_static(self):
        """
        This scraps predicted arrival time for every station. It then modifies
        its structure and forewords it to Kafka.
        """
        for routes_on_station in self.routes_on_stations_data:

            route_int_id = routes_on_station['route_int_id']
            station_int_id = routes_on_station['station_int_id']

            data = self.w_scraper_ignore.get_json(
                self.conf['static']['url'] +
                '?day=' + self.day +
                '&route_int_id=' + str(route_int_id) +
                '&station_int_id=' + str(station_int_id))

            if data is None:
                continue

            for arrival in data['data']:
                tmp = {
                    'station_int_id': station_int_id,
                    'route_int_id': route_int_id,
                    'arrival_time': arrival['arrival_time']
                }
                self.static_producer.send(tmp)

            self.static_producer.flush()

    def run_station(self):
        """
        This simply sends preloaded data about routes on station and sends it to
        Kafka.
        """
        for routes_on_station in self.routes_on_stations_data:
            self.station_producer.send(routes_on_station)

        self.station_producer.flush()
