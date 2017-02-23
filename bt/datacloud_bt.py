import requests

response = requests.get('https://datacloud-timon.xlab.si/data_access/bt_sensors/velocities_avgs_last/', auth=('username', 'password'), verify='DigiCertSHA2SecureServerCA.crt')

data = {'data':[]}
if response.status_code == 200:
    data = response.json()

print(data)

not_lj = ['BTR0219', 'BTR0218', 'BTR0217', 'BTR0213']

for dist in data['data']:
    if dist['toBtId'] not in not_lj and dist['fromBtId'] not in not_lj:
        s = '{} - {} {} {}'.format(dist['toBtId'], dist['fromBtId'], dist['count'], dist['avgSpeed'])
        print(s)
