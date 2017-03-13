import json

from kafka import KafkaProducer
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '10.30.1.132', 'port': 9200}])
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

producer = KafkaProducer(bootstrap_servers=['192.168.0.60:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

for hit in data['hits']['hits']:
    del hit['_source']['summary']
    hit['_source']['deviceX'] = float(hit['_source']['deviceX'].replace(',', '.'))
    hit['_source']['deviceY'] = float(hit['_source']['deviceY'].replace(',', '.'))
    producer.send('inductive_json', hit['_source'])
