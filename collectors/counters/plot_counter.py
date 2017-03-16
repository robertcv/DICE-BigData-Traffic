import requests

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from cartopy.io.img_tiles import OSM
from collectors import settings

response = requests.get(settings.COUNTERS_URL)

data = {'data': []}
if response.status_code == 200:
    data = response.json()
else:
    exit()

stevec = []
lng = []
lat = []
time = data['Contents'][0]['ModifiedTime']

for point in data['Contents'][0]['Data']['Items']:
    if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and settings.LJ_MIN_LNG < point['x_wgs'] < settings.LJ_MAX_LNG:
        stevec.append(point)
        lng.append(point['x_wgs'])
        lat.append(point['y_wgs'])

imagery = OSM()
plt.figure(figsize=(20, 20), dpi=500)
ax = plt.axes(projection=imagery.crs, )
ax.set_extent((min(lng) - 0.02, max(lng) + 0.02, min(lat) - 0.01, max(lat) + 0.01))

ax.add_image(imagery, 14)

plt.plot(lng, lat, 'bo', transform=ccrs.Geodetic(), markersize=8)

plt.title('Stevci')
plt.savefig(settings.COUNTERS_IMG_DIR + "counters.png")
