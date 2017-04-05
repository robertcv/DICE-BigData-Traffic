import json

from pytraffic.collectors.util import kafka_producer, scraper, files, date_time


class BtSensors(object):
    """
    This combines everything bluetooth sensors related. On init it loads sensors
    data or fetches it from web if it’s older then one day. One can use run
    method to send data to Kafka or use plot method to plot a map of
    sensors location.
    """

    def __init__(self, conf):
        """
        Initialize Kafka producer and web scraper classes. Also load bluetooth
        data.

        Args:
            conf (dict): This dict contains all configurations.

        """
        self.conf = conf['bt_sensors']
        self.producer = kafka_producer.Producer(conf['kafka_host'],
                                                self.conf['kafka_topic'])

        self.w_scraper = scraper.Scraper(
            conf['scraper'],
            auth=(self.conf['timon_username'], self.conf['timon_password']),
            verify=self.conf['timon_crt_file'])

        self.not_lj = self.conf['not_lj']

        self.img_dir = conf['data_dir'] + self.conf['img_dir']
        self.sensors_data_file = conf['data_dir'] + self.conf['data_file']
        self.sensors_data = None

    def get_web_data(self):
        """
        This requests bluetooth data from source url and makes a local copy of
        it.
        """
        self.sensors_data = self.w_scraper.get_json(self.conf['sensors_url'])
        if self.sensors_data is not None:
            files.make_dir(self.sensors_data_file)
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
                                   self.conf['data_age']):
            self.get_web_data()
        else:
            self.get_local_data()

    def run(self):
        """
        This scrapes data from source url. It then modifies its structure and
        forewords it to Kafka.
        """
        data = self.w_scraper.get_json(self.conf['last_url'])
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

                dist['timestampTo'] = date_time.isoformat_to_utc(
                    dist['timestampTo'])
                dist['timestampFrom'] = date_time.isoformat_to_utc(
                    dist['timestampFrom'])

                self.producer.send(dist)
        self.producer.flush()

    def get_plot_data(self):
        """
        This function preparers coordinates and labels for plotting.

        Returns:
             lng Longitude part of points coordinates.
             lat Latitude part of points coordinates.
             labels Points labels.

        """
        labels = []
        lng = []
        lat = []
        for point in self.sensors_data:
            if point['btId'] not in self.not_lj:
                labels.append(point['btId'])
                lng.append(point['loc']['lng'])
                lat.append(point['loc']['lat'])
        return lng, lat, labels

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
        # This import is here so the main collector is not dependent on plot
        # requirements.
        from pytraffic.collectors.util import plot

        lng, lat, labels = self.get_plot_data()

        map_plot = plot.PlotOnMap(lng, lat, title)  # lng, lat, 'BT v Ljubljani'
        map_plot.generate(figsize, dpi, zoom, markersize)  # (18, 18), 400, 14, 5
        map_plot.label(labels, lableoffset, fontsize)  # labels, (0.001, 0.0005), 10
        map_plot.save(self.img_dir, file_name)  # 'bt_lj.png'
