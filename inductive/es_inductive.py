import requests
res = requests.get('http://10.30.1.132:9200/inductive_loops')
print(res.content)
print()

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': '10.30.1.132', 'port': 9200}])
data = es.search(index='inductive_loops', body={
    'size' : 10000,
    "query" : {
        "bool" : {
            'must' : [
                {"range" : { "updated" : { "gte" : 'now-1h' }}}
            ]
        }
    },
    "fields" : ["point", 'locationDescription', 'updated','location',  'id', 'title'],
    "sort" : [
        {'id' : 'asc'},
        {"updated" : "asc"}
    ]
})

print(data)

locations = dict()

for hit in data['hits']['hits']:
    fields = hit['fields']
    locations[fields['location'][0]] = [fields['locationDescription'][0], fields['updated'][0], fields['point'][0]]

for k, v in sorted(locations.items()):
    print(k,v)

print(len(locations))