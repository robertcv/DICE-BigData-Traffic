import requests

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM

response = requests.get('https://opendata.si/promet/counters/')

data = {'data':[]}
if response.status_code == 200:
    data = response.json()
else:
    exit()

min_lng = 14.44
max_lng = 14.6
min_lat = 46.0
max_lat = 46.1

stevec = []
lng = []
lat = []
time = data['Contents'][0]['ModifiedTime']

for point in data['Contents'][0]['Data']['Items']:
    if min_lat<point['y_wgs']<max_lat and min_lng<point['x_wgs']<max_lng:
        stevec.append(point)
        lng.append(point['x_wgs'])
        lat.append(point['y_wgs'])

imagery = OSM()
plt.figure(figsize=(20, 20), dpi=500)
ax = plt.axes(projection=imagery.crs, )
ax.set_extent((min(lng)-0.02, max(lng)+0.02, min(lat)-0.01, max(lat)+0.01))

ax.add_image(imagery, 14)

plt.plot(lng, lat, 'bo', transform=ccrs.Geodetic(), markersize=8)

plt.title('Stevci')
plt.savefig("image/counters.png")