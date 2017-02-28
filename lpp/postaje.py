import csv, json

with open('postaje.json') as data_file:
    json_data = json.load(data_file)

json_data_2 = dict()
for d in json_data['data']:
    tmp = {
        'int_id': d['int_id'],
        'lng': d['geometry']['coordinates'][0],
        'lat': d['geometry']['coordinates'][1]
    }
    json_data_2[d['ref_id']] = tmp

print(json_data_2)

with open('postaje.csv') as f:
    csv_data = list(csv.reader(f))

csv_data_2 = dict()
for d in csv_data:
    tmp = {
        'name': d[1],
        'direction': d[2],
    }
    csv_data_2[d[0]] = tmp

print(csv_data_2)


min_lng = 14.44
max_lng = 14.58
min_lat = 46.0
max_lat = 46.1

ofile = open('postaje_lj.csv', 'w')
writer = csv.writer(ofile, delimiter=',')

with open('postaje.html') as f:
    for html_data in f.readlines():
        id = html_data[16:22]
        if id in json_data_2 and id in csv_data_2:
            if min_lat < json_data_2[id]['lat'] < max_lat and min_lng < json_data_2[id]['lng'] < max_lng:
                writer.writerow([json_data_2[id]['int_id'], id, csv_data_2[id]['name'], csv_data_2[id]['direction'],
                                 json_data_2[id]['lng'], json_data_2[id]['lat']])

ofile.close()