import unittest
import unittest.mock as mock
from lxml import html

from pytraffic.collectors import pollution


@mock.patch('pytraffic.collectors.pollution.AirPollution.__init__',
            mock.Mock(return_value=None))
class AirPollutionTest(unittest.TestCase):
    @mock.patch('pytraffic.collectors.pollution.datetime')
    def test_run(self, mock_datetime):
        ap = pollution.AirPollution()
        today = mock.Mock(**{'day': 28, 'month': 3, 'year': 2017})
        mock_datetime.datetime.today.return_value = today
        ap.w_scraper = mock.Mock()
        ap.w_scraper.get_text.return_value = """<html>
        <table id="air-polution">
            <thead><tr><th>ura</th></tr></thead>
            <tbody><tr><th>00:00</th></tr></tbody>
        </table>
        </html>"""

        ap.process_table = mock.Mock()
        ap.run()

        call = ap.w_scraper.get_text.call_args_list

        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertIn('?source=bezigrad&day=28&month=3&year=2017', args1[0])
        self.assertIn('?source=vosnjakova-tivolska&day=28&month=3&year=2017',
                      args2[0])

        call = ap.process_table.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertIn(today, args1)
        self.assertIn(today, args2)
        self.assertIn('bezigrad', args1)
        self.assertIn('vosnjakova-tivolska', args2)
        self.assertEqual(ap.process_table.call_count, 2)

    @mock.patch('pytraffic.collectors.pollution.datetime')
    def test_process_table(self, mock_datetime):
        ap = pollution.AirPollution()
        text = """<html>
        <table class="mediaTable" id="air-polution" cellspacing="0"
               summary="Podatki o onesnaženosti zraka">
            <caption class="hidden">Onesnaženost zraka</caption>
            <thead>
            <tr>
                <th scope="col" class="time essential persist">ura</th>
                <th scope="col" class="stripe essential">
                    SO<sub>2</sub><br/>
                    &micro;g/m<sup>3</sup><br/>
                    <a href="#norm-so2">(normativi)</a>
                </th>
                <th scope="col" class="stripe essential">
                    NO<br/>
                    &micro;g/m<sup>3</sup><br/>
                </th>
                <th scope="col" class="stripe optional">
                    NO<sub>2</sub><br/>
                    &micro;g/m<sup>3</sup><br/>
                    <a href="#norm-no2">(normativi)</a>
                </th>
                <th scope="col" class="stripe optional">
                    NO<sub>&times;</sub><br/>
                    &micro;g/m<sup>3</sup><br/>
                </th>
                <th scope="col" class="stripe optional">
                    CO<br/>
                    mg/m<sup>3</sup><br/>
                    <a href="#norm-co">(normativi)</a>
                </th>
                <th scope="col" class="stripe">
                    Trdni delci PM<sub>10</sub><br/>
                    &micro;g/m<sup>3</sup><br/>
                    <a href="#norm-pm10">(normativi)</a>
                </th>
                <th scope="col" class="stripe">
                    Temperatura<br/>
                    &deg;C<br/>
                </th>
                <th scope="col" class="stripe">
                    Hitrost vetra<br/>
                    m/s<br/>
                </th>
                <th scope="col" class="stripe">
                    Smer vetra<br/>
                    <br/>
                </th>
                <th scope="col" class="stripe">
                    Vlaga<br/>
                    %<br/>
                </th>
                <th scope="col" class="stripe">
                    Pritisk<br/>
                    mbar<br/>
                </th>
                <th scope="col" class="stripe">
                    Sončno sevanje<br/>
                    W/m<sup>2</sup><br/>
                </th>
            </tr></thead>
            <tbody>
            <tr>
                <th scope="row" class="time">01:00</th>
                <td>11.65</td>
                <td>0</td>
                <td>39.05</td>
                <td>38.75</td>
                <td>?</td>
                <td>35.464</td>
                <td>5.2</td>
                <td>0.93</td>
                <td>SV</td>
                <td>55.5</td>
                <td>990.3</td>
                <td>0</td>
            </tr></tbody></table></html>"""

        etree = html.fromstring(text)
        table, = etree.xpath('.//table[@id="air-polution"]')
        date = mock.Mock(**{'day': 28, 'month': 3, 'year': 2017})
        mock_datetime.datetime.isoformat.return_value = '2017-03-28T16:00:00'
        ap.producer = mock.Mock()
        ap.process_table(table, date, 'bezigrad')

        res = {
            'pm': None, 'paraxylene': None, 'hour': '01:00', 'no': None,
            'windspeed': None, 'nox': None, 'co': None, 'so2': None,
            'solar_radiation': None, 'tolulene': None, 'temperature': None,
            'wind_direction': 11.65, 'humidity': None, 'no2': None,
            'location': 39.05, 'pressure': None,
            'scraped': '2017-03-28T16:00:00', 'benzene': None
        }

        ap.producer.send.assert_called_once_with(res)


if __name__ == '__main__':
    unittest.main()
