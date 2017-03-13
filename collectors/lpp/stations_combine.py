import csv, json

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

min_lng = 14.44
max_lng = 14.58
min_lat = 46.0
max_lat = 46.1

ofile = open('data/stations_lj.csv', 'w')
writer = csv.writer(ofile, delimiter=',')

with open('data/stations_lpp_web.html') as f:
    for html_data in f.readlines():
        id = html_data[16:22]
        if id in ijs_data and id in direction_data:
            if min_lat < ijs_data[id]['lat'] < max_lat and min_lng < ijs_data[id]['lng'] < max_lng:
                writer.writerow(
                    [ijs_data[id]['int_id'], id, direction_data[id]['name'], direction_data[id]['direction'],
                     ijs_data[id]['lng'], ijs_data[id]['lat']])

ofile.close()
