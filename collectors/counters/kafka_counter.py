import json
import requests

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.0.60:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

response = requests.get('https://opendata.si/promet/counters/')

data = {'data': []}
if response.status_code == 200:
    data = response.json()

min_lng = 14.44
max_lng = 14.6
min_lat = 46.0
max_lat = 46.1

stevec = []
lng = []
lat = []

ModifiedTime = data['Contents'][0]['ModifiedTime'][:23]+'Z'

for point in data['Contents'][0]['Data']['Items']:
    if min_lat < point['y_wgs'] < max_lat and min_lng < point['x_wgs'] < max_lng:

        for d in point['Data']:
            tmp = point.copy()

            del tmp['Data']
            tmp['id'] = d['Id']
            tmp['modified'] = ModifiedTime

            for p in d['properties']:
                tmp[p] = d['properties'][p]

            tmp['stevci_stev'] = int(tmp['stevci_stev'])
            tmp['stevci_hit'] = int(tmp['stevci_hit'])
            tmp['stevci_gap'] = float(tmp['stevci_gap'].replace(',', '.'))
            tmp['stevci_stat'] = int(tmp['stevci_stat'])

            producer.send('counter_json', tmp)
