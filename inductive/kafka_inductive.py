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

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

for hit in data['hits']['hits']:
    producer.send('inductive_json', hit['_source'])
