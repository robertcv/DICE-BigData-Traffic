from pytraffic import settings
from pytraffic.collectors.util import kafka_producer, es_search

search_body = {
    "size": 10000,
    "query": {
        "bool": {
            'must': [
                {"range": {"updated": {"gte": "now-15m"}}}
            ]
        }
    }
}

ess = es_search.EsSearch(settings.INDUCTIVE_LOOPS_HOST, settings.INDUCTIVE_LOOPS_PORT, settings.INDUCTIVE_LOOPS_INDEX)
data = ess.get_json(search_body)

producer = kafka_producer.Producer(settings.INDUCTIVE_LOOPS_KAFKA_TOPIC)

for hit in data['hits']['hits']:
    del hit['_source']['summary']
    hit['_source']['deviceX'] = float(hit['_source']['deviceX'].replace(',', '.'))
    hit['_source']['deviceY'] = float(hit['_source']['deviceY'].replace(',', '.'))
    producer.send(hit['_source'])
