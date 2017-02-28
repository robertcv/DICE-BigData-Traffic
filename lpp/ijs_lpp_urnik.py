import csv, json
import requests
import datetime, pytz

with open('postaje_lj.csv') as f:
    csv_data = list(csv.reader(f))

station_data = dict()
for d in csv_data:
    tmp = {
        'station_int_id': int(d[0]),
        'station_ref_id': int(d[1]),
        'station_name': d[2],
        'station_direction': d[3],
        'station_lng': float(d[4]),
        'station_lat': float(d[5])
    }
    station_data[d[0]] = tmp

with open('linije.json') as data_file:
    route_data = json.load(data_file)


station_route = {'data':[]}
arrival_time = {'data':[]}

day = str(round(datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc).timestamp()*1000))

for station_int_id in station_data:

    response = requests.get('http://194.33.12.24/stations/getRoutesOnStation?station_int_id=' + station_int_id)
    if response.status_code!=200:
        print('napaka pri getRoutesOnStation: ' + station_int_id)
        continue
    routes_station_data = response.json()['data']

    for route in routes_station_data:
        route_int_id = str(route['route_int_id'])

        if route_int_id in route_data:

            station_data[station_int_id].update(route_data[route_int_id])
            station_route['data'].append(station_data[station_int_id])

            response = requests.get(
                'http://194.33.12.24/timetables/getArrivalsOnStation?day=' + day + '&route_int_id=' + route_int_id +
                '&station_int_id=' + station_int_id)
            if response.status_code != 200:
                #print('napaka pri getArrivalsOnStation: ' + route_int_id + ' - '+ station_int_id)
                continue
            arrival_data = response.json()['data']

            for arrival in arrival_data:
                tmp = {
                    'station_int_id': int(station_int_id),
                    'route_int_id': int(route_int_id),
                    'arrival_time': arrival['arrival_time']
                }
                arrival_time['data'].append(tmp)


with open('station_route.json', 'w') as outfile:
    json.dump(station_route, outfile)

with open('urnik.json', 'w') as outfile:
    json.dump(arrival_time, outfile)
