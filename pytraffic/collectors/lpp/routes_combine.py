import json

from pytraffic import settings
from pytraffic.collectors.util import scraper

w_scraper = scraper.Scraper()
data = w_scraper.get_json(settings.LPP_ROUTE_GROUPS_URL)

routes = dict()

for l in data['data']:
    if not l['name'].isnumeric() or int(l['name']) > 27:
        continue

    res_data = w_scraper.get_json(settings.LPP_ROUTE_URL + '?route_id=' + l['id'])
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

with open(settings.LPP_ROUTE_FILE, 'w') as outfile:
    json.dump(routes, outfile)
