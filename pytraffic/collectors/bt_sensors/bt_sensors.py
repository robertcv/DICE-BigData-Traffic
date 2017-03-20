import json

from pytraffic import settings
from pytraffic.collectors.util import kafka_producer, scraper, plot, files


class BtSensors:
    def __init__(self):
        self.producer = kafka_producer.Producer(settings.BT_SENSORS_KAFKA_TOPIC)
        self.crt_file = files.file_path(__file__, settings.TIMON_CRT_FILE)
        self.w_scraper = scraper.Scraper(auth=(settings.TIMON_USERNAME, settings.TIMON_PASSWORD), verify=self.crt_file)
        self.not_lj = settings.BT_SENSORS_NOT_USE
        self.sensors_data_file = files.file_path(__file__, settings.BT_SENSORS_DATA_FILE)
        self.sensors_data = None
        self.load_data()

    def get_web_data(self):
        self.sensors_data = self.w_scraper.get_json(settings.BT_SENSORS_URL)
        if self.sensors_data is not None:
            with open(self.sensors_data_file, 'w') as outfile:
                json.dump(self.sensors_data, outfile)
            self.sensors_data = self.sensors_data['data']
        else:
            self.get_local_data()

    def get_local_data(self):
        with open(self.sensors_data_file) as data_file:
            self.sensors_data = json.load(data_file)['data']

    def load_data(self):
        if files.old_or_not_exists(self.sensors_data_file, settings.BT_SENSORS_DATA_AGE):
            self.get_web_data()
        else:
            self.get_local_data()

    def run(self):
        data = self.w_scraper.get_json(settings.BT_SENSORS_LAST_URL)
        for dist in data['data']:
            if dist['toBtId'] not in self.not_lj and dist['fromBtId'] not in self.not_lj:
                sensor_from = next(s for s in self.sensors_data if s["btId"] == dist['fromBtId'])
                sensor_to = next(s for s in self.sensors_data if s["btId"] == dist['toBtId'])

                dist['fromBtLng'] = sensor_from['loc']['lng']
                dist['fromBtLat'] = sensor_from['loc']['lat']
                dist['toBtLng'] = sensor_to['loc']['lng']
                dist['toBtLat'] = sensor_to['loc']['lat']
                dist['distance'] = next(s for s in sensor_from['neighbours'] if s["btId"] == dist['toBtId'])['distance']

                self.producer.send(dist)

    def plot_map(self, title, figsize, dpi, zoom, markersize, lableoffset, fontsize, file_name):
        labels = []
        lng = []
        lat = []

        for point in self.sensors_data:
            if point['btId'] not in self.not_lj:
                labels.append(point['btId'])
                lng.append(point['loc']['lng'])
                lat.append(point['loc']['lat'])

        map = plot.PlotOnMap(lng, lat, title)  # lng, lat, 'BT v Ljubljani'
        map.generate(figsize, dpi, zoom, markersize)  # (18, 18), 400, 14, 5
        map.label(labels, lableoffset, fontsize)  # labels, (0.001, 0.0005), 10
        map.save(files.file_path(__file__, settings.BT_SENSORS_IMG_DIR), file_name)  # 'bt_lj.png'
