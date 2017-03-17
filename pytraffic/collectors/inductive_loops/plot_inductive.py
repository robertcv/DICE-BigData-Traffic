from pytraffic import settings
from pytraffic.collectors.util import es_search, plot


search_body = {
    "size": 10000,
    "query": {
        "bool": {
            "must": [
                {"range": {"updated": {"gte": "now-1h"}}}
            ]
        }
    },
    "fields": ["point", "locationDescription", "updated", "location", ],
    "sort": [
        {"updated": "asc"}
    ]
}

ess = es_search.EsSearch(settings.INDUCTIVE_LOOPS_HOST, settings.INDUCTIVE_LOOPS_PORT, settings.INDUCTIVE_LOOPS_INDEX)
data = ess.get_json(search_body)

locations = dict()
labels = []
lng = []
lat = []

for hit in data['hits']['hits']:
    fields = hit['fields']
    locations[fields['location'][0]] = fields['point'][0]

for k, v in locations.items():
    lat_t, lng_t = v.replace(',', '.').split()
    labels.append(k)
    lng.append(float(lng_t))
    lat.append(float(lat_t))

map = plot.PlotOnMap(lng, lat, 'Inductive loops')
map.generate((20, 20), 500, 14, 5)
map.label(labels, (0.0005, 0.00025), 20)
map.save(settings.INDUCTIVE_LOOPS_IMG_DIR, 'inductive.png')