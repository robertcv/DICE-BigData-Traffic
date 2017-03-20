from pytraffic import settings
from pytraffic.collectors.util import kafka_producer, scraper, plot, files


class TrafficCounter:
    def __init__(self):
        self.producer = kafka_producer.Producer(settings.COUNTERS_KAFKA_TOPIC)
        self.w_scraper = scraper.Scraper()
        self.counters_data = None
        self.load_data()

    def load_data(self):
        self.counters_data = self.w_scraper.get_json(settings.COUNTERS_URL)['Contents'][0]['Data']['Items']

    def run(self):
        self.counters_data = self.w_scraper.get_json(settings.COUNTERS_URL)
        modified = self.counters_data['Contents'][0]['ModifiedTime'][:23] + 'Z'
        self.counters_data = self.counters_data['Contents'][0]['Data']['Items']
        for point in self.counters_data:
            if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and settings.LJ_MIN_LNG < point['x_wgs'] < \
                    settings.LJ_MAX_LNG:

                for d in point['Data']:
                    tmp = point.copy()

                    del tmp['Data']
                    tmp['id'] = d['Id']
                    tmp['modified'] = modified

                    for p in d['properties']:
                        tmp[p] = d['properties'][p]

                    tmp['stevci_stev'] = int(tmp['stevci_stev'])
                    tmp['stevci_hit'] = int(tmp['stevci_hit'])
                    tmp['stevci_gap'] = float(tmp['stevci_gap'].replace(',', '.'))
                    tmp['stevci_stat'] = int(tmp['stevci_stat'])

                    self.producer.send(tmp)

    def plot_map(self, title, figsize, dpi, zoom, markersize, file_name):
        lng = []
        lat = []

        for point in self.counters_data:
            if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and settings.LJ_MIN_LNG < point['x_wgs'] < \
                    settings.LJ_MAX_LNG:
                lng.append(point['x_wgs'])
                lat.append(point['y_wgs'])

        map = plot.PlotOnMap(lng, lat, title)  # (lng, lat, 'Stevci')
        map.generate(figsize, dpi, zoom, markersize)  # ((20, 20), 500, 14, 8)
        map.save(files.file_path(__file__, settings.COUNTERS_IMG_DIR), file_name)  # "counters.png"
