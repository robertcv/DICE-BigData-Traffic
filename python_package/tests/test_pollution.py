import unittest
import unittest.mock as mock
from lxml import html

from pytraffic.collectors import pollution


@mock.patch('pytraffic.collectors.pollution.kafka_producer.Producer')
@mock.patch('pytraffic.collectors.pollution.scraper.Scraper')
class AirPollutionTest(unittest.TestCase):
    conf = {
        'kafka_host': 'host',
        'pollution': {
            'url': 'http://test.si/zrak/',
            'kafka_topic': 'pollution_json',
            'locations': {
                'bezigrad': 1,
                'vosnjakova-tivolska': 3
            }
        },
        'scraper': 'scraper'
    }

    @mock.patch('pytraffic.collectors.pollution.datetime')
    def test_run(self, mock_datetime, mock_s, mock_p):
        today = mock.Mock()
        today.day, today.month, today.year = 28, 3, 2017
        yesterday = mock.Mock()
        yesterday.day, yesterday.month, yesterday.year = 27, 3, 2017

        mock_datetime.timedelta.return_value.__rsub__.return_value = yesterday
        mock_datetime.datetime.now.return_value = today
        mock_s.return_value.get_text.return_value = """<html>
        <div class="data-table">
            <table>
                <tr><th>ura</th></tr>
                <tr><th>00:00</th></tr>
            </table>
        </div></html>"""

        ap = pollution.AirPollution(self.conf)
        ap.process_table = mock.Mock()
        ap.run()

        self.assertEqual(mock_s.return_value.get_text.call_count, 4)
        urls = [args[0] for args, kwargs in
                mock_s.return_value.get_text.call_args_list]
        self.assertIn(
            'http://test.si/zrak/?AirMonitoringPointID=1&Date=27.3.2017', urls)
        self.assertIn(
            'http://test.si/zrak/?AirMonitoringPointID=1&Date=28.3.2017', urls)
        self.assertIn(
            'http://test.si/zrak/?AirMonitoringPointID=3&Date=27.3.2017', urls)
        self.assertIn(
            'http://test.si/zrak/?AirMonitoringPointID=3&Date=28.3.2017', urls)

        self.assertEqual(ap.process_table.call_count, 4)
        calls = [arg for args, kwargs in
                 ap.process_table.call_args_list for arg in args]
        self.assertIn('bezigrad', calls)
        self.assertIn('vosnjakova-tivolska', calls)
        self.assertIn(today, calls)
        self.assertIn(yesterday, calls)

    @mock.patch('pytraffic.collectors.pollution.date_time')
    def test_process_table(self, mock_d, mock_s, mock_p):
        ap = pollution.AirPollution(self.conf)
        text = """<html>
        <div class="data-table">
        <div class="filter-header-content">
            <button class="open-filter">Prikaži kolone</button>
        </div>
        <table class="table-scroll-filter">
            <tr><td>Ura</td>
                <td>SO<sub>2</sub>&micro;g/m<sup>3</sup>(normativi)</td>
                <td>NO<br />&micro;g/m<sup>3</sup></td>
                <td>NO<sub>2</sub>&micro;g/m<sup>3</sup>(normativi)</td>
                <td>NO<sub>&times;</sub>&micro;g/m<sup>3</sup></td>
                <td>CO<br />mg/m<sup>3</sup>(normativi)</td>
                <td>Trdni delci PM<sub>10</sub>&micro;g/m<sup>3</sup>(normativi)</td>
                <td>Temperatura<br />&deg;C</td>
                <td>Hitrost vetra<br />m/s</td>
                <td>Smer vetra<br /></td>
                <td>Vlaga<br />%</td>
                <td>Pritisk<br />mbar</td>
                <td>Sončno sevanje<br />W/m<sup>2</sup></td>
            </tr><tr>
                <td>00:00</td>
                <td>14</td>
                <td>2,35</td>
                <td>62,45</td>
                <td>66</td>
                <td>0,25</td>
                <td>30,076</td>
                <td>12,1</td>
                <td>225</td>
                <td>?</td>
                <td>73,6</td>
                <td>981,3</td>
                <td>0</td>
            </tr><tr>
                <td>01:00</td>
                <td>13,65</td>
                <td>0</td>
                <td>38,45</td>
                <td>38,1</td>
                <td>0,18</td>
                <td>20,291</td>
                <td>11,1</td>
                <td>225</td>
                <td>?</td>
                <td>78,3</td>
                <td>981,1</td>
                <td>0</td>
            </tr><tr class="limits">
                <td>mejne vrednosti</td>
                <td>350</td>
                <td></td>
                <td>200</td>
                <td>50</td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        </table></div></html>"""

        mock_d.hour_minut_to_utc.side_effect = ['2017-04-03T22:00:00Z',
                                                '2017-04-03T23:00:00Z']
        date = mock.Mock()
        etree = html.fromstring(text)
        table, = etree.xpath('.//div[@class="data-table"]/table')
        ap.process_table(table, date, 'bezigrad')

        res1 = {'hour': '00:00', 'tolulene': None, 'nox': 66.0, 'pm': 30.076,
                'so2': 14.0, 'solar_radiation': 0.0, 'co': 0.25,
                'humidity': 73.6, 'paraxylene': None, 'temperature': 12.1,
                'scraped': '2017-04-03T22:00:00Z', 'wind_direction': None,
                'location': 'bezigrad', 'no2': 62.45, 'windspeed': 225.0,
                'pressure': 981.3, 'benzene': None, 'no': 2.35}

        res2 = {'hour': '01:00', 'tolulene': None, 'nox': 38.1, 'pm': 20.291,
                'so2': 13.65, 'solar_radiation': 0.0, 'co': 0.18,
                'humidity': 78.3, 'paraxylene': None, 'temperature': 11.1,
                'scraped': '2017-04-03T23:00:00Z', 'wind_direction': None,
                'location': 'bezigrad', 'no2': 38.45, 'windspeed': 225.0,
                'pressure': 981.1, 'benzene': None, 'no': 0.0}

        call = mock_p.return_value.send.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertEqual(res1, args1[0])
        self.assertEqual(res2, args2[0])


if __name__ == '__main__':
    unittest.main()
