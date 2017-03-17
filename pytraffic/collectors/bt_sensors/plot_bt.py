import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from cartopy.io.img_tiles import OSM
from pytraffic import settings
from pytraffic.collectors.util import scraper

w_scraper = scraper.Scraper(auth=(settings.TIMON_USERNAME, settings.TIMON_PASSWORD), verify=settings.TIMON_CRT_FILE)
data = w_scraper.get_json(settings.BT_SENSORS_URL)

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
# plt.savefig(settings.BT_SENSORS_IMG_DIR + "bt_lj.png")

plt.title('Vse BT')
plt.savefig(settings.BT_SENSORS_IMG_DIR + "vse_bt.png")
