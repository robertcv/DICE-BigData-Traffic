from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': '10.30.1.132', 'port': 9200}])
data = es.search(index='inductive_loops', body={
    'size' : 10000,
    "query" : {
        "bool" : {
            'must' : [
                {"range" : { "updated" : { "gte" : 'now-15m' }}}
            ]
        }
    }
})

from kafka import KafkaProducer
import json
from kafka.client import KafkaClient

client = KafkaClient(bootstrap_servers=['192.168.0.62:9092'])
client.add_topic('inductive_json')

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

for hit in data['hits']['hits']:
    producer.send('inductive_json', hit)