import json

from kafka import KafkaProducer
from elasticsearch import Elasticsearch
from collectors.settings import KAFKA_URL, INDUCTIVE_LOOPS_HOST, INDUCTIVE_LOOPS_PORT, INDUCTIVE_LOOPS_KAFKA_TOPIC

es = Elasticsearch([{'host': INDUCTIVE_LOOPS_HOST, 'port': INDUCTIVE_LOOPS_PORT}])
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

producer = KafkaProducer(bootstrap_servers=[KAFKA_URL], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

for hit in data['hits']['hits']:
    del hit['_source']['summary']
    hit['_source']['deviceX'] = float(hit['_source']['deviceX'].replace(',', '.'))
    hit['_source']['deviceY'] = float(hit['_source']['deviceY'].replace(',', '.'))
    producer.send(INDUCTIVE_LOOPS_KAFKA_TOPIC, hit['_source'])
