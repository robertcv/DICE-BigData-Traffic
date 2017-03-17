import json

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer, scraper

producer = kafka_producer.Producer(settings.BT_SENSORS_KAFKA_TOPIC)

w_scraper = scraper.Scraper(auth=(settings.TIMON_USERNAME, settings.TIMON_PASSWORD), verify=settings.TIMON_CRT_FILE)
data = w_scraper.get_json(settings.BT_SENSORS_LAST_URL)

not_lj = settings.BT_SENSORS_NOT_USE

with open('data/bt_sensors.json') as data_file:
    bt_sensors_data = json.load(data_file)['data']

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
