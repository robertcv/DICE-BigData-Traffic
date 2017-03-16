import requests, json

from time import sleep

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer

with open('data/bt_sensors.json') as data_file:
    bt_sensors_data = json.load(data_file)['data']

n = 20
while n > 0:
    sleep(2)
    try:
        response = requests.get(settings.BT_SENSORS_LAST_URL, auth=(settings.TIMON_USERNAME, settings.TIMON_PASSWORD),
                                verify=settings.TIMON_CRT_FILE, timeout=0.1)
        if response.status_code == 200:
            data = response.json()
            break
    except:
        n -= 1
else:
    exit()

producer = kafka_producer.Producer(settings.BT_SENSORS_KAFKA_TOPIC)

not_lj = settings.BT_SENSORS_NOT_USE

for dist in data['data']:
    if dist['toBtId'] not in not_lj and dist['fromBtId'] not in not_lj:
        sensor_from = next(s for s in bt_sensors_data if s["btId"] == dist['fromBtId'])
        sensor_to = next(s for s in bt_sensors_data if s["btId"] == dist['toBtId'])

        dist['fromBtLng'] = sensor_from['loc']['lng']
        dist['fromBtLat'] = sensor_from['loc']['lat']
        dist['toBtLng'] = sensor_to['loc']['lng']
        dist['toBtLat'] = sensor_to['loc']['lat']
        dist['distance'] = next(s for s in sensor_from['neighbours'] if s["btId"] == dist['toBtId'])['distance']

        producer.send(dist)
