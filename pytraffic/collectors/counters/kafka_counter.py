import requests

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer

producer = kafka_producer.Producer(settings.COUNTERS_KAFKA_TOPIC)

response = requests.get(settings.COUNTERS_URL)

data = {'data': []}
if response.status_code == 200:
    data = response.json()

stevec = []
lng = []
lat = []

ModifiedTime = data['Contents'][0]['ModifiedTime'][:23] + 'Z'

for point in data['Contents'][0]['Data']['Items']:
    if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and settings.LJ_MIN_LNG < point['x_wgs'] < settings.LJ_MAX_LNG:

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

            producer.send(tmp)
