import requests

sql = 'select+*+from+bus_data+where+bus_number==3+limit+20'

s = requests.Session()
s.verify = 'DigiCertSHA2SecureServerCA.crt'
s.auth = ('username', 'password')
response = s.get('https://datacloud-timon.xlab.si/data_access/scrapers/sql/' + sql + '/')

data = {'data':[]}
if response.status_code == 200:
    data = response.json()

print(data)