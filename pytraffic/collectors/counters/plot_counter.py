from pytraffic import settings
from pytraffic.collectors.util import scraper, plot

w_scraper = scraper.Scraper()
data = w_scraper.get_json(settings.COUNTERS_URL)

lng = []
lat = []
time = data['Contents'][0]['ModifiedTime']

for point in data['Contents'][0]['Data']['Items']:
    if settings.LJ_MIN_LAT < point['y_wgs'] < settings.LJ_MAX_LAT and settings.LJ_MIN_LNG < point['x_wgs'] < settings.LJ_MAX_LNG:
        lng.append(point['x_wgs'])
        lat.append(point['y_wgs'])

map = plot.PlotOnMap(lng, lat, 'Stevci')
map.generate((20, 20), 500, 14, 8)
map.save(settings.COUNTERS_IMG_DIR, "counters.png")
