import requests
import json

response = requests.get('https://datacloud-timon.xlab.si/data_access/bt_sensors/sensors/',auth=('username', 'password'), verify='DigiCertSHA2SecureServerCA.crt')

if response.status_code == 200:
    data = response.json()
    with open('bt_sensors.json', 'w') as outfile:
        json.dump(data, outfile)