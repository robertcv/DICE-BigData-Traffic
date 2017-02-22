import requests

s = requests.Session()
s.verify = 'DigiCertSHA2SecureServerCA.crt'
s.auth = ('username', 'password')
response = s.get('https://datacloud-timon.xlab.si/data_access/bt_sensors/sensors/')

data = {'data':[]}
if response.status_code == 200:
    data = response.json()

name = []
lng = []
lat = []

for point in data['data']:
    name.append(point['btId'])
    lng.append(point['loc']['lng'])
    lat.append(point['loc']['lat'])

print(data)