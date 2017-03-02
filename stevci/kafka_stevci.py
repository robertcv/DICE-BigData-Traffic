import json
import requests

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'],
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
time = data['Contents'][0]['ModifiedTime']

for point in data['Contents'][0]['Data']['Items']:
    if min_lat < point['y_wgs'] < max_lat and min_lng < point['x_wgs'] < max_lng:
        producer.send('stevci_json', point)
