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
            'url': 'http://test.si/stanje-okolja/zrak/',
            'kafka_topic': 'pollution_json'
        },
        'scraper': 'scraper'
    }

    @mock.patch('pytraffic.collectors.pollution.datetime')
    def test_run(self, mock_datetime, mock_s, mock_p):
        today = mock.Mock(**{'day': 28, 'month': 3, 'year': 2017})
        mock_datetime.datetime.today.return_value = today
        mock_s.return_value.get_text.return_value = """<html>
        <table id="air-polution">
            <thead><tr><th>ura</th></tr></thead>
            <tbody><tr><th>00:00</th></tr></tbody>
        </table>
        </html>"""

        ap = pollution.AirPollution(self.conf)
        ap.process_table = mock.Mock()
        ap.run()

        self.assertEqual(mock_s.return_value.get_text.call_count, 2)
        call = mock_s.return_value.get_text.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertIn('?source=bezigrad&day=28&month=3&year=2017', args1[0])
        self.assertIn('?source=vosnjakova-tivolska&day=28&month=3&year=2017',
                      args2[0])

        self.assertEqual(ap.process_table.call_count, 2)
        call = ap.process_table.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertIn('bezigrad', args1)
        self.assertIn('vosnjakova-tivolska', args2)

    @mock.patch('pytraffic.collectors.pollution.date_time')
    def test_process_table(self, mock_d, mock_s, mock_p):
        ap = pollution.AirPollution(self.conf)
        text = """<html>
        <table class="mediaTable" id="air-polution" cellspacing="0"
        summary="Podatki o onesnaženosti zraka">
        <caption class="hidden">Onesnaženost zraka</caption>
        <thead><tr>
            <th scope="col" class="time essential persist">ura</th>
            <th scope="col" class="stripe essential">SO<sub>2</sub><br/>&micro;g/m<sup>3</sup><br/><a href="#norm-so2">(normativi)</a></th>
            <th scope="col" class="stripe essential">NO<br/>&micro;g/m<sup>3</sup><br/></th>
            <th scope="col" class="stripe optional">NO<sub>2</sub><br/>&micro;g/m<sup>3</sup><br/><a href="#norm-no2">(normativi)</a></th>
            <th scope="col" class="stripe optional">NO<sub>&times;</sub><br/>&micro;g/m<sup>3</sup><br/></th>
            <th scope="col" class="stripe optional">CO<br/>mg/m<sup>3</sup><br/><a href="#norm-co">(normativi)</a></th>
            <th scope="col" class="stripe">Trdni delci PM<sub>10</sub><br/>&micro;g/m<sup>3</sup><br/><a href="#norm-pm10">(normativi)</a></th>
            <th scope="col" class="stripe">Temperatura<br/>&deg;C<br/></th>
            <th scope="col" class="stripe">Hitrost vetra<br/>m/s<br/></th>
            <th scope="col" class="stripe">Smer vetra<br/><br/></th>
            <th scope="col" class="stripe">Vlaga<br/>%<br/></th>
            <th scope="col" class="stripe">Pritisk<br/>mbar<br/></th>
            <th scope="col" class="stripe">Sončno sevanje<br/>W/m<sup>2</sup><br/></th>
        </tr></thead><tbody><tr class="first">
            <th scope="row" class="time">00:00</th>
            <td>5.95</td>
            <td>0</td>
            <td>38.15</td>
            <td>37.15</td>
            <td>0.23</td>
            <td>41.097</td>
            <td>14</td>
            <td>0.21</td>
            <td>V</td>
            <td>44.7</td>
            <td>982.5</td>
            <td>0</td>
        </tr><tr>
            <th scope="row" class="time">01:00</th>
            <td>5.95</td>
            <td>0</td>
            <td>55.5</td>
            <td>54.85</td>
            <td>0.27</td>
            <td>42.024</td>
            <td>13.1</td>
            <td>0.65</td>
            <td>Z</td>
            <td>48.3</td>
            <td>982.5</td>
            <td>0</td>
        </tr><tr class="limits">
        <th scope="row" class="limit">mejne vrednosti</th>
            <td>350</td>
            <td></td>
            <td>200</td>
            <td></td>
            <td></td>
            <td>50</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr></tbody></table></html>"""

        mock_d.hour_minut_to_utc.side_effect = ['2017-04-03T22:00:00Z',
                                                '2017-04-03T23:00:00Z']

        etree = html.fromstring(text)
        table, = etree.xpath('.//table[@id="air-polution"]')
        ap.process_table(table, 'bezigrad')

        res1 = {'pm': 41.097, 'co': 0.23, 'no2': 38.15, 'windspeed': 0.21,
                'location': None, 'so2': 5.95, 'nox': 37.15,
                'temperature': 14.0, 'humidity': 44.7, 'tolulene': None,
                'hour': '00:00', 'wind_direction': 'V',
                'solar_radiation': None, 'benzene': None, 'pressure': 982.5,
                'paraxylene': None, 'scraped': '2017-04-03T22:00:00Z',
                'no': 0.0}

        res2 = {'pm': 42.024, 'co': 0.27, 'no2': 55.5, 'windspeed': 0.65,
                'location': None, 'so2': 5.95, 'nox': 54.85,
                'temperature': 13.1, 'humidity': 48.3, 'tolulene': None,
                'hour': '01:00', 'wind_direction': 'Z',
                'solar_radiation': None, 'benzene': None, 'pressure': 982.5,
                'paraxylene': None, 'scraped': '2017-04-03T23:00:00Z',
                'no': 0.0}

        call = mock_p.return_value.send.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertEqual(res1, args1[0])
        self.assertEqual(res2, args2[0])


if __name__ == '__main__':
    unittest.main()
