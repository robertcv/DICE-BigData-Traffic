import requests, datetime, re, json

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

from lxml import html


def process_table(table, date, source):
    isoformat_date = datetime.date.isoformat(date)
    header_row, = table.xpath('.//thead/tr')

    headers = [re.sub('[\r\n\t]', '', header_cell.text_content().strip()) for header_cell in header_row.xpath('./th')]

    english = {'ura': 'hour',
               'SO2µg/m3(normativi)': 'so2',
               'NOµg/m3': 'no',
               'NO2µg/m3(normativi)': 'no2',
               'NO×µg/m3': 'nox',
               'O3µg/m3(normativi)': 'ozone',
               'COmg/m3(normativi)': 'co',
               'Trdni delci PM10µg/m3(normativi)': 'pm',
               'Temperatura°C': 'temperature',
               'Hitrost vetram/s': 'windspeed',
               'Smer vetra': 'wind_direction',
               'Vlaga%': 'humidity',
               'Pritiskmbar': 'pressure',
               'SonÄ\x8dno sevanjeW/m2': 'solar_radiation',
               'Benzenµg/m3(normativi)': 'benzene',
               'Toluenµg/m3': 'tolulene',
               'Paraksilenµg/m3': 'paraxylene', }

    english_headers = [english[header] for header in headers if header in english]

    english_headers.append('scraped')
    english_headers.append('location')

    value_rows = table.xpath('.//tbody/tr[not(@class="limits") and not(@class="alarms")]')
    all_rows = []

    for value_row in value_rows:
        row = []

        for value_cell in value_row.xpath('./th|td'):
            row.append(value_cell.text_content().strip())

        row.append(isoformat_date)
        row.append(source)
        all_rows.append(dict(zip(english_headers, row)))

    return all_rows[-1]


url = 'http://www.ljubljana.si/si/zivljenje-v-ljubljani/okolje-prostor-bivanje/stanje-okolja/zrak/' \
      '?source={}&day={}&month={}&year={}'

date = datetime.datetime.today() - datetime.timedelta(hours=3)

for source in ['bezigrad', 'vosnjakova-tivolska']:
    response = requests.get(url.format(source, date.day, date.month, date.year))
    etree = html.fromstring(response.text)
    table, = etree.xpath('.//table[@id="air-polution"]')
    print(process_table(table, date, source))
    producer.send('pollution_json', process_table(table, date, source))
