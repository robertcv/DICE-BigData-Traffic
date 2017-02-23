import requests
res = requests.get('http://10.30.1.132:9200/inductive_loops')
print(res.content)
print()

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': '10.30.1.132', 'port': 9200}])
data = es.search(index='inductive_loops', body={
    'size' : 300,
    "query" : {
        "bool" : {
            'must' : [
                {"range" : { "updated" : { "gte" : 'now-20m' }}}
            ]
        }
    },
    "fields" : ["point", 'locationDescription', 'updated', 'id', 'title'],
    "sort" : [
        {"updated" : "desc"},
    ]
})

for hit in data['hits']['hits']:
    fields = hit['fields']

    s = '{} {} {}'.format(fields['id'], fields['locationDescription'], fields['title'])
    print(s)

print(data)