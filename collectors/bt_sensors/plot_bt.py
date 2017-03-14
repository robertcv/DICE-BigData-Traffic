import requests
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from cartopy.io.img_tiles import OSM
from collectors.settings import BT_SENSORS_URL, TIMON_USERNAME, TIMON_PASSWORD, BT_SENSORS_NOT_USE

response = requests.get(BT_SENSORS_URL, auth=(TIMON_USERNAME, TIMON_PASSWORD), verify='crt/datacloud.crt')

if response.status_code == 200:
    data = response.json()
else:
    exit()

name = []
lng = []
lat = []

# not_lj = BT_SENSORS_NOT_USE
not_lj = []

for point in data['data']:
    if point['btId'] not in not_lj:
        name.append(point['btId'])
        lng.append(point['loc']['lng'])
        lat.append(point['loc']['lat'])

imagery = OSM()
plt.figure(figsize=(15, 15), dpi=600)
ax = plt.axes(projection=imagery.crs, )
ax.set_extent((min(lng) - 0.02, max(lng) + 0.02, min(lat) - 0.01, max(lat) + 0.01))

ax.add_image(imagery, 12)

plt.plot(lng, lat, 'bo', transform=ccrs.Geodetic(), markersize=5)

for i in range(len(lng)):
    plt.text(lng[i] + 0.001, lat[i] + 0.0005, name[i], horizontalalignment='left', fontsize=10,
             transform=ccrs.Geodetic())

# plt.title('BT v Ljubljani')
# plt.savefig("image/bt_lj.png")

plt.title('Vse BT')
plt.savefig("./image/vse_bt.png")
