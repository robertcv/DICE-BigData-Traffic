import json, csv

from .. import settings
from .util import kafka_producer, scraper, files, date_time


class LppTraffic:
    def __init__(self):
        self.day = date_time.today_timestamp()
        self.w_scraper = scraper.Scraper(timeout=1)
        self.w_scraper_ignore = scraper.Scraper(timeout=1, ignore_status_code=True)
        self.live_producer = kafka_producer.Producer(settings.LPP_LIVE_KAFKA_TOPIC)
        self.station_producer = kafka_producer.Producer(settings.LPP_STATION_KAFKA_TOPIC)
        self.static_producer = kafka_producer.Producer(settings.LPP_STATIC_KAFKA_TOPIC)
        self.stations_data_file = files.file_path(__file__, settings.LPP_STATION_FILE)
        self.stations_data = None
        self.routes_data_file = files.file_path(__file__, settings.LPP_ROUTE_FILE)
        self.routes_data = None
        self.routes_on_stations_data_file = files.file_path(__file__, settings.LPP_ROUTES_ON_STATION_FILE)
        self.routes_on_stations_data = []
        self.load_routes_on_stations_data()

    def get_local_data(self, file):
        with open(file) as data_file:
            return json.load(data_file)

    def get_web_stations_data(self):
        ijs_station_data = self.w_scraper.get_json(settings.LPP_STATION_URL)

        data = dict()

        direction_file = files.file_path(__file__, settings.LPP_STATION_DIRECTION_FILE)
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
            if station['ref_id'] in direction_data_dict \
                    and settings.LJ_MIN_LAT < station['geometry']['coordinates'][1] < settings.LJ_MAX_LAT \
                    and settings.LJ_MIN_LNG < station['geometry']['coordinates'][0] < settings.LJ_MAX_LNG:
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
        ijs_group_data = self.w_scraper.get_json(settings.LPP_ROUTE_GROUPS_URL)

        data = dict()
        for group in ijs_group_data['data']:
            if group['name'].isnumeric() and int(group['name']) <= 27:

                ijs_route_data = self.w_scraper_ignore.get_json(settings.LPP_ROUTE_URL + '?route_id=' + group['id'])

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
        if files.old_or_not_exists(self.stations_data_file, settings.LPP_DATA_AGE):
            self.get_web_stations_data()
        else:
            self.stations_data = self.get_local_data(self.stations_data_file)

    def load_routes_data(self):
        if files.old_or_not_exists(self.routes_data_file, settings.LPP_DATA_AGE):
            self.get_web_routes_data()
        else:
            self.routes_data = self.get_local_data(self.routes_data_file)

    def get_web_routes_on_stations_data(self):
        data = []
        for station_int_id in self.stations_data:

            ijs_station_data = self.w_scraper_ignore.get_json(
                settings.LPP_ROUTES_ON_STATION_URL + '?station_int_id=' + station_int_id)

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
        self.load_stations_data()
        self.load_routes_data()

        if files.old_or_not_exists(self.routes_on_stations_data_file, settings.LPP_DATA_AGE):
            self.get_web_routes_on_stations_data()
        else:
            self.routes_on_stations_data = self.get_local_data(self.routes_on_stations_data_file)['data']

    def run_live(self):
        for station_int_id in self.stations_data:

            data = self.w_scraper.get_json(settings.LPP_LIVE_URL + '?station_int_id=' + station_int_id)

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
        for routes_on_station in self.routes_on_stations_data:

            route_int_id = routes_on_station['route_int_id']
            station_int_id = routes_on_station['station_int_id']

            data = self.w_scraper_ignore.get_json(settings.LPP_STATIC_URL + '?day=' + self.day + '&route_int_id=' + str(
                route_int_id) + '&station_int_id=' + str(station_int_id))
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
        for routes_on_station in self.routes_on_stations_data:
            self.station_producer.send(routes_on_station)

        self.static_producer.flush()
