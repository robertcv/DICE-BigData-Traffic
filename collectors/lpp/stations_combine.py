import csv, json

from collectors.settings import LPP_STATION_FILE, LJ_MIN_LNG, LJ_MAX_LNG, LJ_MIN_LAT, LJ_MAX_LAT

with open('data/stations_ijs.json') as data_file:
    ijs_file = json.load(data_file)

ijs_data = dict()
for d in ijs_file['data']:
    tmp = {
        'int_id': d['int_id'],
        'lng': d['geometry']['coordinates'][0],
        'lat': d['geometry']['coordinates'][1]
    }
    ijs_data[d['ref_id']] = tmp

with open('data/stations_directions.csv') as f:
    direction_file = list(csv.reader(f))

direction_data = dict()
for d in direction_file:
    tmp = {
        'name': d[1],
        'direction': d[2],
    }
    direction_data[d[0]] = tmp

ofile = open('data/' + LPP_STATION_FILE, 'w')
writer = csv.writer(ofile, delimiter=',')

with open('data/stations_lpp_web.html') as f:
    for html_data in f.readlines():
        id = html_data[16:22]
        if id in ijs_data and id in direction_data:
            if LJ_MIN_LAT < ijs_data[id]['lat'] < LJ_MAX_LAT and LJ_MIN_LNG < ijs_data[id]['lng'] < LJ_MAX_LNG:
                writer.writerow(
                    [ijs_data[id]['int_id'], id, direction_data[id]['name'], direction_data[id]['direction'],
                     ijs_data[id]['lng'], ijs_data[id]['lat']])

ofile.close()
