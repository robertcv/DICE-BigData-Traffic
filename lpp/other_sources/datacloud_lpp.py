import requests

sql = 'select+*+from+bus_data+order+by+retrieval_date+desc+limit+10'

s = requests.Session()
s.verify = 'datacloud.crt'
s.auth = ('username', 'password')
response = s.get('https://datacloud-timon.xlab.si/data_access/scrapers/sql/' + sql + '/')

data = {'data':[]}
if response.status_code == 200:
    data = response.json()

print(data)