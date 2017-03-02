import json
import requests
from time import sleep

response = requests.get('http://194.33.12.24/routes/getRouteGroups')
data = response.json()

routes = dict()

for l in data['data']:
    if not l['name'].isnumeric() or int(l['name']) > 27:
        continue

    sleep(0.01)
    response = requests.get('http://194.33.12.24/routes/getRoutes?route_id=' + l['id'])
    res_data = response.json()
    if res_data['success']:
        for d in res_data['data']:
            tmp = {
                'route_num': int(l['name']),
                'route_int_id': d['int_id']
            }
            name = d['name']
            if ';' in name and 'osnovna' in name:
                name = name[:name.find(';')]
            elif ';' in name:
                continue

            if name[1] == ' ':
                tmp['route_num_sub'] = name[0]
                name = name[2:]
            else:
                tmp['route_num_sub'] = ''

            tmp['route_name'] = name
            routes[d['int_id']] = tmp

with open('data/routes_ijs.json', 'w') as outfile:
    json.dump(routes, outfile)
