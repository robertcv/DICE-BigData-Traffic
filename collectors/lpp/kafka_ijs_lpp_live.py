import csv, json
import requests

from kafka import KafkaProducer
from collectors.settings import KAFKA_URL, LPP_LIVE_URL, LPP_LIVE_KAFKA_TOPIC, LPP_STATION_FILE

producer = KafkaProducer(bootstrap_servers=[KAFKA_URL], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

with open('data/' + LPP_STATION_FILE) as f:
    station_data = list(csv.reader(f))

for station in station_data:

    station_int_id = station[0]

    response = requests.get(LPP_LIVE_URL + '?station_int_id=' + station_int_id)
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
        producer.send(LPP_LIVE_KAFKA_TOPIC, tmp)
    producer.flush()
