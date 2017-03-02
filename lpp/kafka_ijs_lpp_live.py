import csv, json
import requests

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

with open('data/stations_lj.csv') as f:
    station_data = list(csv.reader(f))

for station in station_data:

    station_int_id = station[0]

    response = requests.get('http://194.33.12.24/timetables/liveBusArrival?station_int_id=' + station_int_id)
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
        producer.send('lpp_live_json', tmp)
