from elasticsearch import Elasticsearch
from pytraffic import settings
from pytraffic.collectors.util import kafka_producer


es = Elasticsearch([{'host': settings.INDUCTIVE_LOOPS_HOST, 'port': settings.INDUCTIVE_LOOPS_PORT}])
data = es.search(index='inductive_loops', body={
    'size': 10000,
    "query": {
        "bool": {
            'must': [
                {"range": {"updated": {"gte": 'now-15m'}}}
            ]
        }
    }
})

producer = kafka_producer.Producer(settings.INDUCTIVE_LOOPS_KAFKA_TOPIC)

for hit in data['hits']['hits']:
    del hit['_source']['summary']
    hit['_source']['deviceX'] = float(hit['_source']['deviceX'].replace(',', '.'))
    hit['_source']['deviceY'] = float(hit['_source']['deviceY'].replace(',', '.'))
    producer.send(hit['_source'])
