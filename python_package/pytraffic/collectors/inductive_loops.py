from pytraffic.collectors.util import kafka_producer, es_search


class InductiveLoops(object):
    """
    This combines everything inductive loops related. One can use run
    method to send data to Kafka or use plot method to plot a
    map of inductive loops.

    Attributes:
        kafka_search_body (dict): Dictionary with the search setting for data to
            be forwarded to Kafka.
        map_search_body (dict): Dictionary with the search setting for inductive
            oops location.

    """
    kafka_search_body = {
        "size": 10000,
        "query": {
            "bool": {
                'must': [
                    {"range": {"updated": {"gte": "now-15m"}}}
                ]
            }
        }
    }

    map_search_body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {"range": {"updated": {"gte": "now-1h"}}}
                ]
            }
        },
        "fields": ["point", "locationDescription", "updated", "location", ],
        "sort": [
            {"updated": "asc"}
        ]
    }

    def __init__(self, conf):
        """
        Initialize Kafka producer and Elasticsearch connection.

        Args:
            conf (dict): This dict contains all configurations.

        """
        self.conf = conf['inductive_loops']
        self.producer = kafka_producer.Producer(conf['kafka_host'],
                                                self.conf['kafka_topic'])
        self.ess = es_search.EsSearch(self.conf['es_host'],
                                      self.conf['es_port'],
                                      self.conf['es_index'])

    def run(self):
        """
        Query the elasticsearch to get inductive loops data. Modify data
        structure and send it to Kafka.
        """
        data = self.ess.get_json(self.kafka_search_body)
        for hit in data['hits']['hits']:
            del hit['_source']['summary']
            hit['_source']['deviceX'] = float(
                hit['_source']['deviceX'].replace(',', '.'))
            hit['_source']['deviceY'] = float(
                hit['_source']['deviceY'].replace(',', '.'))
            self.producer.send(hit['_source'])

    def get_plot_data(self):
        """
        This function preparers coordinates and labels for plotting.

        Returns:
             lng Longitude part of points coordinates.
             lat Latitude part of points coordinates.
             labels Points labels.

        """
        data = self.ess.get_json(self.map_search_body)
        locations = dict()
        labels = []
        lng = []
        lat = []

        # If we have duplicate location this overrides itself and we end up
        # with only one copy of it.
        for hit in data['hits']['hits']:
            fields = hit['fields']
            locations[fields['location'][0]] = fields['point'][0]

        for k, v in locations.items():
            lat_t, lng_t = v.replace(',', '.').split()
            labels.append(k)
            lng.append(float(lng_t))
            lat.append(float(lat_t))

        return lng, lat, labels

    def plot_map(self, title, figsize, dpi, zoom, markersize, lableoffset,
                 fontsize, file_name):
        """
        This function crates a map of inductive loops location.

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

        map_plot = plot.PlotOnMap(lng, lat, title)  # 'Inductive loops'
        map_plot.generate(figsize, dpi, zoom, markersize)  # (20, 20), 500, 14, 5
        map_plot.label(labels, lableoffset, fontsize)  # (0.0005, 0.00025), 20
        map_plot.save(self.conf['img_dir'], file_name)  # 'inductive.png'
