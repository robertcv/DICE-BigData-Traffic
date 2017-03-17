import csv, json
import datetime, pytz

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer, scraper


station_producer = kafka_producer.Producer(settings.LPP_STATION_KAFKA_TOPIC)
static_producer = kafka_producer.Producer(settings.LPP_STATIC_KAFKA_TOPIC)

w_scraper_station = scraper.Scraper(retries=1)
w_scraper_static = scraper.Scraper(retries=1, ignore_status_code=True)

with open(settings.LPP_STATION_FILE) as f:
    station_file = list(csv.reader(f))

station_data = dict()
for d in station_file:
    tmp = {
        'station_int_id': int(d[0]),
        'station_ref_id': int(d[1]),
        'station_name': d[2],
        'station_direction': d[3],
        'station_lng': float(d[4]),
        'station_lat': float(d[5])
    }
    station_data[d[0]] = tmp

with open(settings.LPP_ROUTE_FILE) as data_file:
    route_data = json.load(data_file)

date = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)

day = str(round(date.timestamp() * 1000))

for station_int_id in station_data:

    data = w_scraper_station.get_json(settings.LPP_STATION_URL + '?station_int_id=' + station_int_id)

    for route in data['data']:
        route_int_id = str(route['route_int_id'])

        if route_int_id in route_data:

            station_data[station_int_id].update(route_data[route_int_id])
            station_data[station_int_id]['scraped'] = datetime.datetime.isoformat(date)
            station_producer.send(station_data[station_int_id])

            data = w_scraper_static.get_json(
                settings.LPP_STATIC_URL + '?day=' + day + '&route_int_id=' + route_int_id + '&station_int_id=' + station_int_id)
            if data is None:
                # print('napaka pri getArrivalsOnStation: ' + route_int_id + ' - '+ station_int_id + ' status code: ' + str(w_scraper_static.last_status_code))
                continue

            for arrival in data['data']:
                tmp = {
                    'station_int_id': int(station_int_id),
                    'route_int_id': int(route_int_id),
                    'arrival_time': arrival['arrival_time']
                }
                static_producer.send(tmp)

            static_producer.flush()
