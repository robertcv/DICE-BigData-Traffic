import csv

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer, scraper


producer = kafka_producer.Producer(settings.LPP_LIVE_KAFKA_TOPIC)

w_scraper = scraper.Scraper(retries=1)

with open(settings.LPP_STATION_FILE) as f:
    station_data = list(csv.reader(f))

for station in station_data:

    station_int_id = station[0]
    data = w_scraper.get_json(settings.LPP_LIVE_URL + '?station_int_id=' + station_int_id)

    for route in data['data']:
        tmp = {
            'station_int_id': int(station_int_id),
            'route_int_id': route['route_int_id'],
            'arrival_time': route['local_timestamp']
        }
        producer.send(tmp)
    producer.flush()
