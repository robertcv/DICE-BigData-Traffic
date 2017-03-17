from elasticsearch import Elasticsearch, ElasticsearchException
from pytraffic.collectors.util import exceptions


class EsSearch:
    def __init__(self, host, port, index):
        self.host = host
        self.port = port
        self.index = index
        self.es = None
        self.connect()

    def connect(self):
        try:
            self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        except ElasticsearchException:
            raise exceptions.ConnectionError('Elasticsearch on {}'.format(self.host + ':' + self.port))

    def get_json(self, body):
        try:
            data = self.es.search(index=self.index, body=body)
            return data
        except ElasticsearchException:
            raise exceptions.SearchError('{} on index {}'.format(body, self.index))
