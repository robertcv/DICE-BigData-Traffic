import csv
import requests

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer


producer = kafka_producer.Producer(settings.LPP_LIVE_KAFKA_TOPIC)

with open(settings.LPP_STATION_FILE) as f:
    station_data = list(csv.reader(f))

for station in station_data:

    station_int_id = station[0]

    response = requests.get(settings.LPP_LIVE_URL + '?station_int_id=' + station_int_id)
    if response.status_code != 200:
        # print('napaka pri liveBusArrival: ' + station_int_id)
        continue
    routes_station_data = response.json()['data']

    for route in routes_station_data:
        tmp = {
            'station_int_id': int(station_int_id),
            'route_int_id': route['route_int_id'],
            'arrival_time': route['local_timestamp']
        }
        producer.send(tmp)
    producer.flush()
