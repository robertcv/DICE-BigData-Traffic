import json

from .. import settings
from .util import kafka_producer, scraper, plot, files


class BtSensors:
    """
    This combines everything bluetooth sensors related. On init it loads sensors
    data or fetches it from web if it’s older then one day. One can use run
    method to send data to Kafka or use plot method to plot a map of
    sensors location.
    """

    def __init__(self):
        """
        Initialize Kafka producer and web scraper classes. Also load bluetooth
        data.
        """
        self.producer = kafka_producer.Producer(settings.BT_SENSORS_KAFKA_TOPIC)
        self.crt_file = files.file_path(__file__, settings.TIMON_CRT_FILE)
        self.w_scraper = scraper.Scraper(
            auth=(settings.TIMON_USERNAME, settings.TIMON_PASSWORD),
            verify=self.crt_file)
        self.not_lj = settings.BT_SENSORS_NOT_USE
        self.sensors_data_file = files.file_path(__file__,
                                                 settings.BT_SENSORS_DATA_FILE)
        self.sensors_data = None
        self.load_data()

    def get_web_data(self):
        """
        This requests bluetooth data from source url and makes a local copy of
        it.
        """
        self.sensors_data = self.w_scraper.get_json(settings.BT_SENSORS_URL)
        if self.sensors_data is not None:
            with open(self.sensors_data_file, 'w') as outfile:
                json.dump(self.sensors_data, outfile)
            self.sensors_data = self.sensors_data['data']
        else:
            self.get_local_data()

    def get_local_data(self):
        """
        This loads the local copy of bluetooth sensors data.
        """
        with open(self.sensors_data_file) as data_file:
            self.sensors_data = json.load(data_file)['data']

    def load_data(self):
        """
        We check if we have a not to old local copy of bluetooth sensors data.
        If yes we load it from local file, if not we get the data from source
        url and then create a local copy.
        """
        if files.old_or_not_exists(self.sensors_data_file,
                                   settings.BT_SENSORS_DATA_AGE):
            self.get_web_data()
        else:
            self.get_local_data()

    def run(self):
        """
        This scrapes data from source url. It then modifies its structure and
        forewords it to Kafka.
        """
        data = self.w_scraper.get_json(settings.BT_SENSORS_LAST_URL)
        for dist in data['data']:
            if dist['toBtId'] not in self.not_lj and \
                    dist['fromBtId'] not in self.not_lj:

                sensor_from = next(s for s in self.sensors_data if
                                   s["btId"] == dist['fromBtId'])

                sensor_to = next(s for s in self.sensors_data if
                                 s["btId"] == dist['toBtId'])

                dist['fromBtLng'] = sensor_from['loc']['lng']
                dist['fromBtLat'] = sensor_from['loc']['lat']
                dist['toBtLng'] = sensor_to['loc']['lng']
                dist['toBtLat'] = sensor_to['loc']['lat']

                dist['distance'] = next(s for s in sensor_from['neighbours'] if
                                        s["btId"] == dist['toBtId'])['distance']

                self.producer.send(dist)

    def plot_map(self, title, figsize, dpi, zoom, markersize, lableoffset,
                 fontsize, file_name):
        """
        This function crates a map of bluetooth sensors location.

        Args:
            title (str): Plot title.
            figsize (tuple of int): Figure size.
            dpi (int): Dots per inch.
            zoom (int): Map zoom.
            markersize (int): Size of dots.
            offset (tuple of float): Offset of labels from dots.
            fontsize (int): Size of labels.
            file_name (str): Name of saved file.

        """
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
        map.save(settings.BT_SENSORS_IMG_DIR, file_name)  # 'bt_lj.png'
