from pytraffic import settings
from pytraffic.collectors.util import scraper, plot

w_scraper = scraper.Scraper(auth=(settings.TIMON_USERNAME, settings.TIMON_PASSWORD), verify=settings.TIMON_CRT_FILE)
data = w_scraper.get_json(settings.BT_SENSORS_URL)

labels = []
lng = []
lat = []

# not_lj = BT_SENSORS_NOT_USE
not_lj = []

for point in data['data']:
    if point['btId'] not in not_lj:
        labels.append(point['btId'])
        lng.append(point['loc']['lng'])
        lat.append(point['loc']['lat'])

# map = plot.PlotOnMap(lng, lat, 'BT v Ljubljani')
map = plot.PlotOnMap(lng, lat, 'Vse BT')
map.generate((15, 15), 600, 12, 5)
map.label(labels, (0.001, 0.0005), 10)
map.save(settings.BT_SENSORS_IMG_DIR, 'vse_bt.png')
# map.save(settings.BT_SENSORS_IMG_DIR, 'bt_lj.png')