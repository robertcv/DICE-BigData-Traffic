from .. import settings
from .util import kafka_producer, es_search, plot


class InductiveLoops:
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

    def __init__(self):
        """
        Initialize Kafka producer and Elasticsearch connection.
        """
        self.producer = kafka_producer.Producer(
            settings.INDUCTIVE_LOOPS_KAFKA_TOPIC)
        self.ess = es_search.EsSearch(settings.INDUCTIVE_LOOPS_HOST,
                                      settings.INDUCTIVE_LOOPS_PORT,
                                      settings.INDUCTIVE_LOOPS_INDEX)

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

        map = plot.PlotOnMap(lng, lat, title)  # 'Inductive loops'
        map.generate(figsize, dpi, zoom, markersize)  # (20, 20), 500, 14, 5
        map.label(labels, lableoffset, fontsize)  # (0.0005, 0.00025), 20
        map.save(settings.INDUCTIVE_LOOPS_IMG_DIR, file_name)  # 'inductive.png'
