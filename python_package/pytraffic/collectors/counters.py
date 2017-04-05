from pytraffic.collectors.util import kafka_producer, scraper


class TrafficCounter(object):
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
        self.img_dir = conf['data_dir'] + self.conf['img_dir']

    def load_data(self):
        """
        This loads data from the web. This data is needed if we wont to plot
        counters location before we use run method.

        Returns:
            Dictionary of counters data.
        """
        return self.w_scraper.get_json(
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
        self.producer.flush()

    def get_plot_data(self):
        """
        This function preparers coordinates for plotting.

        Returns:
             lng Longitude part of points coordinates.
             lat Latitude part of points coordinates.

        """
        if self.counters_data is None:
            self.counters_data = self.load_data()

        lng = []
        lat = []

        for point in self.counters_data:
            if self.conf_lj['min_lat'] < point['y_wgs'] < self.conf_lj['max_lat'] and \
                    self.conf_lj['min_lng'] < point['x_wgs'] < self.conf_lj['max_lng']:
                lng.append(point['x_wgs'])
                lat.append(point['y_wgs'])
        return lng, lat


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
        # This import is here so the main collector is not dependent on plot
        # requirements.
        from pytraffic.collectors.util import plot

        lng, lat = self.get_plot_data()

        map_plot = plot.PlotOnMap(lng, lat, title)  # (lng, lat, 'Stevci')
        map_plot.generate(figsize, dpi, zoom, markersize)  # ((20, 20), 500, 14, 8)
        map_plot.save(self.img_dir, file_name)  # "counters.png"
