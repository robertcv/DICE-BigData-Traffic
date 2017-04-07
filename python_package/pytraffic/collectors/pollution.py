import datetime
import re

from lxml import html
from pytraffic.collectors.util import kafka_producer, scraper, date_time


class AirPollution(object):
    """
    This combines everything pollution related. One can use run method to send
    data to Kafka.

    Attributes:
        english (dict): Dictionary of table header mapping.
        default (dict): Default dictionary for pollution data.

    """
    english = {'Ura': 'hour',
               'SO2µg/m3(normativi)': 'so2',
               'NOµg/m3': 'no',
               'NO2µg/m3(normativi)': 'no2',
               'NO×µg/m3': 'nox',
               'COmg/m3(normativi)': 'co',
               'Trdni delci PM10µg/m3(normativi)': 'pm',
               'Temperatura°C': 'temperature',
               'Hitrost vetram/s': 'windspeed',
               'Smer vetra': 'wind_direction',
               'Vlaga%': 'humidity',
               'Pritiskmbar': 'pressure',
               'Sončno sevanjeW/m2': 'solar_radiation',
               'Benzenµg/m3(normativi)': 'benzene',
               'Toluenµg/m3': 'tolulene',
               'Paraksilenµg/m3': 'paraxylene'}

    default = {'hour': None,
               'so2': None,
               'no': None,
               'no2': None,
               'nox': None,
               'co': None,
               'pm': None,
               'temperature': None,
               'windspeed': None,
               'wind_direction': None,
               'humidity': None,
               'pressure': None,
               'solar_radiation': None,
               'benzene': None,
               'tolulene': None,
               'paraxylene': None,
               'scraped': None,
               'location': None}

    def __init__(self, conf):
        """
        Initialize Kafka producer and web scraper classes.

        Args:
            conf (dict): This dict contains all configurations.

        """
        self.conf = conf['pollution']
        self.producer = kafka_producer.Producer(conf['kafka_host'],
                                                self.conf['kafka_topic'])
        self.w_scraper = scraper.Scraper(conf['scraper'])

    def process_table(self, table, date, location):
        """
        This function processes html table of data and sends it to Kafka.

        Args:
            table (str): String of html code which contains the air pollution
                table.
            date (:obj:datetime): Datetime object for the date.
            location (str): Location where the pollution data is collected.

        """
        rows = table.xpath(
            './tr[not(@class="limits") and not(@class="alarms")]')

        headers = [re.sub('[\r\n\t]', '', header_cell.text_content().strip())
                   for header_cell in rows[0].xpath('./td')]

        # map Slovenian headers to English
        english_headers = [self.english[header] for header in headers if
                           header in self.english]

        english_headers.append('scraped')
        english_headers.append('location')

        all_rows = []

        for value_row in rows[1:]:
            row = []

            for value_cell in value_row.xpath('./td'):
                v = value_cell.text_content().strip()
                if ',' in v:
                    v = v.replace(',', '.')
                try:
                    v = float(v)
                except ValueError:
                    pass
                if v == '?':
                    v = None
                row.append(v)

            row.append(None)
            row.append(location)
            all_rows.append(dict(zip(english_headers, row)))

        # update the default dict with the fetched data, rearrange it and send
        # it to Kafka
        for row in all_rows:
            tmp = self.default.copy()
            tmp.update(row)
            hour, minute = tmp['hour'].split(':')
            tmp['scraped'] = date_time.hour_minut_to_utc(date, int(hour),
                                                         int(minute))
            self.producer.send(tmp)
        self.producer.flush()

    def run(self):
        """
        This fetches the html code from source url. It then calls process_table
        to further process the code and sends data Kafka.
        """
        url = self.conf['url'] + '?AirMonitoringPointID={}&Date={}.{}.{}'
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        for l in self.conf['locations']:
            for d in [yesterday, today]:
                text = self.w_scraper.get_text(
                    url.format(self.conf['locations'][l], d.day, d.month,
                               d.year))
                etree = html.fromstring(text)
                table, = etree.xpath('.//div[@class="data-table"]/table')
                self.process_table(table, d, l)
