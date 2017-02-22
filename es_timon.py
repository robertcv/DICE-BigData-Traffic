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
                {"range" : { "updated" : { "gte" : 'now-3h' }}}
            ]
        }
    },
    "fields" : ["point", 'locationDescription', 'updated', 'id', 'title'],
    "sort" : [
        {"updated" : "asc"},
    ]
})

print(data)

locations = dict()

for hit in data['hits']['hits']:
    fields = hit['fields']
    locations[fields['id'][0]] = [fields['locationDescription'], fields['updated'], fields['title']]

for l in locations.items():
    print(l)