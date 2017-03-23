from .. import settings
from .util import kafka_producer, scraper, plot


class TrafficCounter:
    """
    This combines everything traffic counters related. One can use run
    method to send data to Kafka or use plot method to plot a
    map of counters location.
    """

    def __init__(self):
        """
        Initialize Kafka producer and web scraper classes. Also load counters
        data.
        """
        self.producer = kafka_producer.Producer(settings.COUNTERS_KAFKA_TOPIC)
        self.w_scraper = scraper.Scraper()
        self.counters_data = None
        self.load_data()

    def load_data(self):
        """
        This loads data from the web. This data is needed if we wont to plot
        counters location before we use run method.
        """
        self.counters_data = self.w_scraper.get_json(
            settings.COUNTERS_URL)['Contents'][0]['Data']['Items']

    def run(self):
        """
        This scrapes data from source url. Then it checks if the counter is
        inside the set area. If it is then we modify it structure and foreward
        it to Kafka.
        """
        self.counters_data = self.w_scraper.get_json(settings.COUNTERS_URL)
        modified = self.counters_data['Contents'][0]['ModifiedTime'][:23] + 'Z'
        self.counters_data = self.counters_data['Contents'][0]['Data']['Items']
        for point in self.counters_data:
            if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and \
                    settings.LJ_MIN_LNG < point['x_wgs'] < settings.LJ_MAX_LNG:

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
            if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and \
                    settings.LJ_MIN_LNG < point['x_wgs'] < settings.LJ_MAX_LNG:
                lng.append(point['x_wgs'])
                lat.append(point['y_wgs'])

        map = plot.PlotOnMap(lng, lat, title)  # (lng, lat, 'Stevci')
        map.generate(figsize, dpi, zoom, markersize)  # ((20, 20), 500, 14, 8)
        map.save(settings.COUNTERS_IMG_DIR, file_name)  # "counters.png"
