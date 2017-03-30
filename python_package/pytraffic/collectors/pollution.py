import datetime
import re

from lxml import html
from pytraffic.collectors.util import kafka_producer, scraper


class AirPollution(object):
    """
    This combines everything pollution related. One can use run method to send
    data to Kafka.

    Attributes:
        english (dict): Dictionary of table header mapping.
        default (dict): Default dictionary for pollution data.

    """
    english = {'ura': 'hour',
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
               'SonÄ\x8dno sevanjeW/m2': 'solar_radiation',
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
            date (:obj:datetime): Datetime object of today.
            location (str): Location where the pollution data is collected.

        """
        header_row, = table.xpath('.//thead/tr')

        headers = [re.sub('[\r\n\t]', '', header_cell.text_content().strip())
                   for header_cell in
                   header_row.xpath('./th')]

        # map Slovenian headers to English
        english_headers = [self.english[header] for header in headers if
                           header in self.english]

        english_headers.append('scraped')
        english_headers.append('location')

        value_rows = table.xpath(
            './/tbody/tr[not(@class="limits") and not(@class="alarms")]')
        all_rows = []

        # get all table rows
        for value_row in value_rows:
            row = []

            for value_cell in value_row.xpath('./th|td'):
                v = value_cell.text_content().strip()
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
            isoformat_date = datetime.datetime.isoformat(
                date.replace(hour=int(hour), minute=int(minute), second=0,
                             microsecond=0))
            tmp['scraped'] = isoformat_date
            self.producer.send(tmp)

    def run(self):
        """
        This fetches the html code from source url. It then calls process_table
        to further process the code and sends data Kafka.
        """
        url = self.conf['url'] + '?source={}&day={}&month={}&year={}'
        date = datetime.datetime.today()
        for location in ['bezigrad', 'vosnjakova-tivolska']:
            text = self.w_scraper.get_text(
                url.format(location, date.day, date.month, date.year))
            etree = html.fromstring(text)
            table, = etree.xpath('.//table[@id="air-polution"]')
            self.process_table(table, date, location)
