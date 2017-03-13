import matplotlib.pyplot as plt

import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM

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
    "fields" : ["point", 'locationDescription', 'updated','location',],
    "sort" : [
        {"updated" : "asc"}
    ]
})

locations = dict()
name = []
lng = []
lat = []

for hit in data['hits']['hits']:
    fields = hit['fields']
    locations[fields['location'][0]] = fields['point'][0]

for k, v in locations.items():
    lat_t, lng_t = v.replace(',', '.').split()
    name.append(k)
    lng.append(float(lng_t))
    lat.append(float(lat_t))

imagery = OSM()
plt.figure(figsize=(20, 20), dpi=500)
ax = plt.axes(projection=imagery.crs, )
ax.set_extent((min(lng)-0.02, max(lng)+0.02, min(lat)-0.01, max(lat)+0.01))

ax.add_image(imagery, 14)

plt.plot(lng, lat, 'bo', transform=ccrs.Geodetic(),
         markersize=5)

for i in range(len(lng)):
    plt.text(lng[i]+0.0005, lat[i]+0.00025, name[i],
         horizontalalignment='left', fontsize=20,
         transform=ccrs.Geodetic())

plt.title('Inductive loops')
plt.savefig("image/inductive.png")