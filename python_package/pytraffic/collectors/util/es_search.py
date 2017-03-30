from elasticsearch import Elasticsearch, ElasticsearchException
from pytraffic.collectors.util import exceptions


class EsSearch(object):
    """
    This class is a wrapper around the official elasticsearch module.
    Its main purpose is to catch connection or search exceptions.
    """

    def __init__(self, host, port, index):
        """
        Initialize ElasticSearch connection.

        Args:
            host (str): Elasticsearch machine hostname.
            port (str): Elasticsearch port.
            index (str): Elasticsearch index of the desirable data.

        """
        self.host = host
        self.port = port
        self.index = index
        self.es = self.connect()

    def connect(self):
        """
        Start a connection to elasticsearch.

        Returns:
            Elasticsearch object used to search for data.

        Raises:
            ConnectionError: If connection couldn't be established.

        """
        try:
            return Elasticsearch([{'host': self.host, 'port': self.port}])
        except ElasticsearchException:
            raise exceptions.ConnectionError('Elasticsearch on {}'.format(self.host + ':' + self.port))

    def get_json(self, body):
        """
        Search for data on elasticsearch.

        Args:
            body (dict): Dictionary with the search body.

        Returns:
            dict: Result data.

        Raises:
            SearchError: If there is an error with parsing the body.

        """
        try:
            data = self.es.search(index=self.index, body=body)
            return data
        except ElasticsearchException:
            raise exceptions.SearchError('{} on index {}'.format(body, self.index))
