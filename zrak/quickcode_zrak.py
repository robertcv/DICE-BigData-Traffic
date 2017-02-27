import requests
from datetime import datetime, timedelta

t = datetime.now() - timedelta(hours=1)
hour = t.strftime("%H:00")
scraped = t.strftime("%Y-%m-%d")

#bezigrad
response = requests.get('https://ds-ec2.scraperwiki.com/5b5caao/j8mbheckizajnzk/sql/?q=select%20*%0Afrom%20bezigrad%0Awhere%20hour%3D%22' + hour + '%22%20and%20scraped%3D%22' + scraped + '%22%0A')

data = {'data':[]}
if response.status_code == 200 and response.json()!=[]:
    data = response.json()


data[0]['location'] = 'bezigrad'
print(data[0])


t = datetime.now() - timedelta(hours=2)
hour = t.strftime("%H:00")
scraped = t.strftime("%Y-%m-%d")

#vosnjakova-tivolska
response = requests.get('https://ds-ec2.scraperwiki.com/5b5caao/j8mbheckizajnzk/sql/?q=select%20*%0Afrom %22vosnjakova-tivolska%22%0Awhere%20hour%3D%22' + hour + '%22%20and%20scraped%3D%22' + scraped + '%22%0A')

data = {'data':[]}
if response.status_code == 200 and response.json()!=[]:
    data = response.json()


data[0]['location'] = 'vosnjakova-tivolska'
print(data[0])