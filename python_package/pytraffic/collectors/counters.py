from .util import kafka_producer, scraper, plot


class TrafficCounter:
    """
    This combines everything traffic counters related. One can use run
    method to send data to Kafka or use plot method to plot a
    map of counters location.
    """

    def __init__(self, conf):
        """
        Initialize Kafka producer and web scraper classes. Also load counters
        data.

        Args:
            conf (dict): This dict contains all configurations.

        """
        self.conf = conf['counters']
        self.conf_lj = conf['location']
        self.producer = kafka_producer.Producer(conf['kafka_host'],
                                                self.conf['kafka_topic'])
        self.w_scraper = scraper.Scraper(conf['scraper'])
        self.counters_data = None
        self.load_data()

    def load_data(self):
        """
        This loads data from the web. This data is needed if we wont to plot
        counters location before we use run method.
        """
        self.counters_data = self.w_scraper.get_json(
                self.conf['url'])['Contents'][0]['Data']['Items']

    def run(self):
        """
        This scrapes data from source url. Then it checks if the counter is
        inside the set area. If it is then we modify it structure and foreward
        it to Kafka.
        """
        self.counters_data = self.w_scraper.get_json(self.conf['url'])
        modified = self.counters_data['Contents'][0]['ModifiedTime'][:23] + 'Z'
        self.counters_data = self.counters_data['Contents'][0]['Data']['Items']
        for point in self.counters_data:
            if self.conf_lj['min_lat'] < point['y_wgs'] < self.conf_lj['max_lat'] and \
                    self.conf_lj['min_lng'] < point['x_wgs'] < self.conf_lj['max_lng']:

                for d in point['Data']:
                    tmp = point.copy()

                    del tmp['Data']
                    tmp['id'] = d['Id']
                    tmp['modified'] = modified

                    for p in d['properties']:
                        tmp[p] = d['properties'][p]

                    tmp['stevci_stev'] = int(tmp['stevci_stev'])
                    tmp['stevci_hit'] = int(tmp['stevci_hit'])
                    tmp['stevci_gap'] = float(
                        tmp['stevci_gap'].replace(',', '.'))
                    tmp['stevci_stat'] = int(tmp['stevci_stat'])

                    self.producer.send(tmp)

    def plot_map(self, title, figsize, dpi, zoom, markersize, file_name):
        """
        This function crates a map of traffic counters location.

        Args:
            title (str): Plot title.
            figsize (tuple of int): Figure size.
            dpi (int): Dots per inch.
            zoom (int): Map zoom.
            markersize (int): Size of dots.
            file_name (str): Name of saved file.

        """
        lng = []
        lat = []

        for point in self.counters_data:
            if self.conf_lj['min_lat'] < point['y_wgs'] < self.conf_lj['max_lat'] and \
                    self.conf_lj['min_lng'] < point['x_wgs'] < self.conf_lj['max_lng']:
                lng.append(point['x_wgs'])
                lat.append(point['y_wgs'])

        map = plot.PlotOnMap(lng, lat, title)  # (lng, lat, 'Stevci')
        map.generate(figsize, dpi, zoom, markersize)  # ((20, 20), 500, 14, 8)
        map.save(self.conf['img_dir'], file_name)  # "counters.png"
