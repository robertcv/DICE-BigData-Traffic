import unittest
import unittest.mock as mock

from pytraffic.collectors import lpp


@mock.patch('pytraffic.collectors.lpp.LppTraffic.__init__',
            mock.Mock(return_value=None))
class LppTrafficTest(unittest.TestCase):
    @mock.patch('pytraffic.collectors.lpp.open')
    @mock.patch('pytraffic.collectors.lpp.json')
    def test_get_local_data(self, mock_json, mock_open):
        lt = lpp.LppTraffic()
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_json.load.return_value = {'data': [1, 2, 3]}
        self.assertEqual(lt.get_local_data('file.json'), {'data': [1, 2, 3]})
        mock_open.assert_called_once_with('file.json')
        mock_json.load.assert_called_once_with(data_file)

    @mock.patch('pytraffic.collectors.lpp.files')
    def test_load_stations_data(self, mock_files):
        lt = lpp.LppTraffic()
        lt.get_web_stations_data = mock.Mock()
        lt.get_local_data = mock.Mock(return_value={'data': [1, 2, 3]})
        lt.stations_data_file = 'file.json'

        mock_files.old_or_not_exists.return_value = False
        lt.load_stations_data()
        lt.get_web_stations_data.assert_not_called()
        lt.get_local_data.assert_called_once()

        mock_files.old_or_not_exists.return_value = True
        lt.load_stations_data()
        lt.get_web_stations_data.assert_called_once()
        lt.get_local_data.assert_called_with('file.json')
        self.assertEqual(lt.stations_data, {'data': [1, 2, 3]})

    @mock.patch('pytraffic.collectors.lpp.files')
    def test_load_routes_data(self, mock_files):
        lt = lpp.LppTraffic()
        lt.get_web_routes_data = mock.Mock()
        lt.get_local_data = mock.Mock(return_value={'data': [1, 2, 3]})
        lt.routes_data_file = 'file.json'

        mock_files.old_or_not_exists.return_value = False
        lt.load_routes_data()
        lt.get_web_routes_data.assert_not_called()
        lt.get_local_data.assert_called_once()

        mock_files.old_or_not_exists.return_value = True
        lt.load_routes_data()
        lt.get_web_routes_data.assert_called_once()
        lt.get_local_data.assert_called_with('file.json')
        self.assertEqual(lt.routes_data, {'data': [1, 2, 3]})

    @mock.patch('pytraffic.collectors.lpp.files')
    def test_load_routes_on_stations_data(self, mock_files):
        lt = lpp.LppTraffic()
        lt.get_web_routes_on_stations_data = mock.Mock()
        lt.get_local_data = mock.Mock(return_value={'data': [1, 2, 3]})
        lt.load_stations_data = mock.Mock()
        lt.load_routes_data = mock.Mock()
        lt.routes_on_stations_data_file = 'file.json'

        mock_files.old_or_not_exists.return_value = False
        lt.load_routes_on_stations_data()
        lt.get_web_routes_on_stations_data.assert_not_called()
        lt.get_local_data.assert_called_once()

        mock_files.old_or_not_exists.return_value = True
        lt.load_routes_on_stations_data()
        lt.get_web_routes_on_stations_data.assert_called_once()
        lt.get_local_data.assert_called_with('file.json')

        self.assertEqual(lt.routes_on_stations_data, [1, 2, 3])
        self.assertEqual(lt.load_stations_data.call_count, 2)
        self.assertEqual(lt.load_routes_data.call_count, 2)

    @mock.patch('pytraffic.collectors.lpp.date_time')
    @mock.patch('pytraffic.collectors.lpp.files')
    @mock.patch('pytraffic.collectors.lpp.csv')
    @mock.patch('pytraffic.collectors.lpp.open')
    @mock.patch('pytraffic.collectors.lpp.json')
    def test_get_web_stations_data(self, mock_json, mock_open, mock_csv,
                                   mock_files, mock_time):
        lt = lpp.LppTraffic()
        lt.stations_data_file = 'file.json'
        lt.w_scraper = mock.Mock()
        lt.w_scraper.get_json.return_value = {
            "success": True,
            "data": [
                {
                    "int_id": 3335,
                    "ref_id": "502013",
                    "name": "Ambrožev trg",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            14.5172493587762,
                            46.0495728420941
                        ]
                    }
                },
                {
                    "int_id": 3334,
                    "ref_id": "502014",
                    "name": "Ambrožev trg",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            14.5168919025372,
                            46.0495752574493
                        ]
                    }
                },
                {
                    "int_id": 3558,
                    "ref_id": "505141",
                    "name": "GROSUPLJE",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            14.6525158244926,
                            45.9560914146265
                        ]
                    }
                }
            ]
        }
        mock_files.file_path.return_value = 'file'
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_csv.reader.return_value = [
            ['502013', 'Ambrožev trg', '→'],
            ['502014', 'Ambrožev trg', ''],
            ['505141', 'Grosuplje', '→']
        ]
        mock_time.now_isoformat.return_value = '2017-03-28T16:00:00.000000'

        lt.get_web_stations_data()

        res = {
            '3335':
                {
                    'station_ref_id': '502013',
                    'station_name': 'Ambrožev trg',
                    'station_lng': 14.5172493587762,
                    'station_lat': 46.0495728420941,
                    'scraped': '2017-03-28T16:00:00.000000',
                    'station_direction': '→',
                    'station_int_id': 3335
                },
            '3334':
                {
                    'station_ref_id': '502014',
                    'station_name': 'Ambrožev trg',
                    'station_lng': 14.5168919025372,
                    'station_lat': 46.0495752574493,
                    'scraped': '2017-03-28T16:00:00.000000',
                    'station_direction': '',
                    'station_int_id': 3334
                }
        }

        call = mock_open.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertEqual(args1, ('file',))
        mock_csv.reader.assert_called_once_with(data_file)
        self.assertEqual(args2, ('file.json', 'w'))
        mock_json.dump.assert_called_with(res, data_file)

    @mock.patch('pytraffic.collectors.lpp.date_time')
    @mock.patch('pytraffic.collectors.lpp.open')
    @mock.patch('pytraffic.collectors.lpp.json')
    def test_get_web_routes_data(self, mock_json, mock_open, mock_time):
        lt = lpp.LppTraffic()
        lt.routes_data_file = 'file.json'
        lt.w_scraper = mock.Mock()
        lt.w_scraper.get_json.return_value = {
            "success": True,
            "data": [
                {
                    "id": "dc78be0d-0c14-43f1-886f-69101eba48fb",
                    "name": "3"
                },
                {
                    "id": "659b8748-bfa7-4a8e-8b70-a552b40c5152",
                    "name": "6B"
                },
                {
                    "id": "a043812e-7541-46d4-9911-49f6a5b71c17",
                    "name": "46"
                }
            ]
        }
        lt.w_scraper_ignore = mock.Mock()
        lt.w_scraper_ignore.get_json.return_value = {
            "success": True,
            "data": [
                {
                    "id": "d1bee690-f3b0-49cf-a61f-bb65607ce0d2",
                    "route_parent_id": "9027ea9d-4a91-493f-890a-d9a39271e600",
                    "int_id": 1100,
                    "opposite_route_int_id": 1098,
                    "name": "LITOSTROJ;  arhiv",
                    "length": 9779.85840405003,
                    "route_parent_name": "RUDNIK - LITOSTROJ"
                },
                {
                    "id": "e8f428e7-877b-4fae-8bd0-4eb7a911d463",
                    "route_parent_id": "db781c1d-c7c6-4887-84dd-f1b400752a1c",
                    "int_id": 1553,
                    "opposite_route_int_id": 1096,
                    "name": "B LITOSTROJ;  osnovna",
                    "length": 15001.617297584155,
                    "route_parent_name": "B ŠKOFLJICA - LITOSTROJ"
                },
                {
                    "id": "c975b8c2-6758-42ea-8fa1-87c00cdf9970",
                    "route_parent_id": "2339913c-c993-4b30-a2e4-01b8e7b23542",
                    "int_id": 1561,
                    "opposite_route_int_id": None,
                    "name": "GARAŽA;  osnovna",
                    "length": 8572.889271426635,
                    "route_parent_name": "RUDNIK - GARAŽA"
                },
                {
                    "id": "3cb8ceaf-fe81-41f8-b6e3-feee8c796030",
                    "route_parent_id": "9027ea9d-4a91-493f-890a-d9a39271e600",
                    "int_id": 1562,
                    "opposite_route_int_id": 1557,
                    "name": "LITOSTROJ;  osnovna",
                    "length": 9778.44206408395,
                    "route_parent_name": "RUDNIK - LITOSTROJ"
                }
            ]
        }
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_time.now_isoformat.return_value = '2017-03-28T16:00:00.000000'

        lt.get_web_routes_data()

        res = {
            '1553':
                {
                    'scraped': '2017-03-28T16:00:00.000000',
                    'route_int_id': 1553,
                    'route_num_sub': 'B',
                    'route_num': 3,
                    'route_name': 'LITOSTROJ'
                },
            '1562':
                {
                    'scraped': '2017-03-28T16:00:00.000000',
                    'route_int_id': 1562,
                    'route_num_sub': '',
                    'route_num': 3,
                    'route_name': 'LITOSTROJ'
                },
            '1561':
                {
                    'scraped': '2017-03-28T16:00:00.000000',
                    'route_int_id': 1561,
                    'route_num_sub': '',
                    'route_num': 3,
                    'route_name': 'GARAŽA'
                }
        }

        lt.w_scraper.get_json.assert_called_once()
        lt.w_scraper_ignore.get_json.assert_called_once()
        args, kwargs = lt.w_scraper_ignore.get_json.call_args
        self.assertIn('?route_id=dc78be0d-0c14-43f1-886f-69101eba48fb', args[0])
        mock_open.assert_called_once_with('file.json', 'w')
        mock_json.dump.assert_called_with(res, data_file)

    @mock.patch('pytraffic.collectors.lpp.date_time')
    @mock.patch('pytraffic.collectors.lpp.open')
    @mock.patch('pytraffic.collectors.lpp.json')
    def test_get_web_routes_on_stations_data(self, mock_json, mock_open,
                                             mock_time):
        lt = lpp.LppTraffic()
        lt.routes_on_stations_data_file = 'file.json'
        lt.stations_data = {
            "3641": {
                "station_ref_id": "803212",
                "scraped": "2017-03-21T00:00:00+00:00",
                "station_lng": 14.4918072201637,
                "station_name": "Kovinarska",
                "station_direction": "",
                "station_int_id": 3641,
                "station_lat": 46.0804464528947
            }
        }
        lt.routes_data = {
            '1553': {
                'scraped': '2017-03-28T16:00:00.000000',
                'route_int_id': 1553,
                'route_num_sub': 'B',
                'route_num': 3,
                'route_name': 'LITOSTROJ'
            },
            '1562': {
                'scraped': '2017-03-28T16:00:00.000000',
                'route_int_id': 1562,
                'route_num_sub': '',
                'route_num': 3,
                'route_name': 'LITOSTROJ'
            },
            '1561': {
                'scraped': '2017-03-28T16:00:00.000000',
                'route_int_id': 1561,
                'route_num_sub': '',
                'route_num': 3,
                'route_name': 'GARAŽA'
            }
        }
        lt.w_scraper_ignore = mock.Mock()
        lt.w_scraper_ignore.get_json.return_value = {
            "success": True,
            "data": [
                {
                    "route_int_id": 1097
                },
                {
                    "route_int_id": 1100
                },
                {
                    "route_int_id": 1562,
                    "name": "LITOSTROJ;  osnovna"
                },
                {
                    "route_int_id": 1553,
                    "name": "B LITOSTROJ;  osnovna"
                },
                {
                    "route_int_id": 1386,
                    "name": "C. STOŽICE P+R;  osnovna"
                },
                {
                    "route_int_id": 1641,
                    "name": "L LITOSTROJ"
                }
            ]
        }
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_time.now_isoformat.return_value = '2017-03-28T16:00:00.000000'

        lt.get_web_routes_on_stations_data()

        res = [
            {
                'route_num_sub': '',
                'station_lng': 14.4918072201637,
                'station_ref_id': '803212',
                'route_int_id': 1562,
                'route_num': 3,
                'station_int_id': 3641,
                'scraped': '2017-03-28T16:00:00.000000',
                'station_lat': 46.0804464528947,
                'station_name': 'Kovinarska',
                'route_name': 'LITOSTROJ',
                'station_direction': ''
            },
            {
                'route_num_sub': 'B',
                'station_lng': 14.4918072201637,
                'station_ref_id': '803212',
                'route_int_id': 1553,
                'route_num': 3,
                'station_int_id': 3641,
                'scraped': '2017-03-28T16:00:00.000000',
                'station_lat': 46.0804464528947,
                'station_name': 'Kovinarska',
                'route_name': 'LITOSTROJ',
                'station_direction': ''
            }
        ]

        lt.w_scraper_ignore.get_json.assert_called_once()
        args, kwargs = lt.w_scraper_ignore.get_json.call_args
        self.assertIn('?station_int_id=3641', args[0])
        mock_open.assert_called_once_with('file.json', 'w')
        mock_json.dump.assert_called_with({'data': res}, data_file)

    def test_run_live(self):
        lt = lpp.LppTraffic()
        lt.stations_data = {
            "1944": {
                "station_ref_id": "601012",
                "scraped": "2017-03-21T00:00:00+00:00",
                "station_lng": 14.5028208626036,
                "station_name": "Konzorcij",
                "station_direction": "",
                "station_int_id": 1944,
                "station_lat": 46.0512362310992
            }
        }
        lt.w_scraper = mock.Mock()
        lt.w_scraper.get_json.return_value = {
            "success": True,
            "data": [
                {
                    "station_int_id": 1944,
                    "route_int_id": 730,
                    "vehicle_int_id": 101,
                    "route_number": 27,
                    "route_name": "  N.S. RUDNIK",
                    "eta": 0,
                    "validity": 60,
                    "utc_timestamp": "2017-03-29T08:23:46.000Z",
                    "local_timestamp": "2017-03-29 10:23:46.000"
                },
                {
                    "station_int_id": 1944,
                    "route_int_id": 737,
                    "vehicle_int_id": 595,
                    "route_number": 2,
                    "route_name": "  NOVE JARŠE",
                    "eta": 0,
                    "validity": 60,
                    "utc_timestamp": "2017-03-29T08:19:28.000Z",
                    "local_timestamp": "2017-03-29 10:19:28.000"
                },
                {
                    "station_int_id": 1944,
                    "route_int_id": 1564,
                    "vehicle_int_id": 393,
                    "route_number": 6,
                    "route_name": "  DOLGI MOST P+R",
                    "eta": 18,
                    "validity": 120,
                    "utc_timestamp": "2017-03-29T08:25:03.000Z",
                    "local_timestamp": "2017-03-29 10:25:03.000"
                }
            ]
        }
        lt.live_producer = mock.Mock()
        res1 = {
            "station_int_id": 1944,
            "route_int_id": 730,
            "arrival_time": "2017-03-29 10:23:46.000"
        }
        res2 = {
            "station_int_id": 1944,
            "route_int_id": 737,
            "arrival_time": "2017-03-29 10:19:28.000"
        }

        lt.run_live()

        lt.w_scraper.get_json.assert_called_once()
        args, kwargs = lt.w_scraper.get_json.call_args
        self.assertIn('?station_int_id=1944', args[0])
        self.assertEqual(lt.live_producer.send.call_count, 2)
        args1, kwargs1 = lt.live_producer.send.call_args_list[0]
        self.assertEqual(args1[0], res1)
        args2, kwargs2 = lt.live_producer.send.call_args_list[1]
        self.assertEqual(args2[0], res2)
        lt.live_producer.flush.assert_called_once()

    def test_run_static(self):
        lt = lpp.LppTraffic()
        lt.routes_on_stations_data = [
            {
                "station_ref_id": "803211",
                "scraped": "2017-03-21T00:00:00+00:00",
                "route_name": "RUDNIK",
                "station_lng": 14.4913580625216,
                "station_name": "Kovinarska",
                "route_num_sub": "",
                "station_direction": "\u2192",
                "station_int_id": 3642,
                "route_int_id": 1098,
                "route_num": 3,
                "station_lat": 46.0803964420806
            }
        ]
        lt.day = '1490745600000'
        lt.w_scraper_ignore = mock.Mock()
        lt.w_scraper_ignore.get_json.return_value = {
            "success": True,
            "data": [
                {
                    "_id": "5866da8eea14860adc10df23",
                    "id": "51f0b517-d068-4062-a543-e7643c025780",
                    "int_id": 5203613,
                    "station_id": "8ecaf199-e1f5-45bb-9208-8d9c152cf8e1",
                    "station_int_id": 3642,
                    "route_departure_id": "5655e1f6-8e3d-4f86-adee-cbacff5d3e4b",
                    "route_departure_int_id": 410079,
                    "arrival_time": "2017-03-29T04:56:00.000Z"
                },
                {
                    "_id": "5866dab4ea14860adc10e0a8",
                    "id": "96b7fb25-75cb-4248-96a7-e6fec2955afa",
                    "int_id": 5203535,
                    "station_id": "8ecaf199-e1f5-45bb-9208-8d9c152cf8e1",
                    "station_int_id": 3642,
                    "route_departure_id": "0aafccbf-947d-44a3-bdd7-2249251372d3",
                    "route_departure_int_id": 410075,
                    "arrival_time": "2017-03-29T05:31:00.000Z"
                }
            ]
        }
        lt.static_producer = mock.Mock()
        res1 = {
            "station_int_id": 3642,
            "route_int_id": 1098,
            "arrival_time": "2017-03-29T04:56:00.000Z"
        }
        res2 = {
            "station_int_id": 3642,
            "route_int_id": 1098,
            "arrival_time": "2017-03-29T05:31:00.000Z"
        }

        lt.run_static()

        lt.w_scraper_ignore.get_json.assert_called_once()
        args, kwargs = lt.w_scraper_ignore.get_json.call_args
        self.assertIn(
            '?day=1490745600000&route_int_id=1098&station_int_id=3642', args[0])
        self.assertEqual(lt.static_producer.send.call_count, 2)
        args1, kwargs1 = lt.static_producer.send.call_args_list[0]
        self.assertEqual(args1[0], res1)
        args2, kwargs2 = lt.static_producer.send.call_args_list[1]
        self.assertEqual(args2[0], res2)
        lt.static_producer.flush.assert_called_once()

    def test_run_station(self):
        lt = lpp.LppTraffic()
        lt.routes_on_stations_data = [
            {
                "station_ref_id": "103061",
                "scraped": "2017-03-21T00:00:00+00:00",
                "route_name": "GARA\u017dA",
                "station_lng": 14.5072916018955,
                "station_name": "Pohorskega bataljona",
                "route_num_sub": "",
                "station_direction": "\u2192",
                "station_int_id": 2211,
                "route_int_id": 1047,
                "route_num": 14,
                "station_lat": 46.0824088609516
            },
            {
                "station_ref_id": "103061",
                "scraped": "2017-03-21T00:00:00+00:00",
                "route_name": "BOKALCE",
                "station_lng": 14.5072916018955,
                "station_name": "Pohorskega bataljona",
                "route_num_sub": "",
                "station_direction": "\u2192",
                "station_int_id": 2211,
                "route_int_id": 987,
                "route_num": 14,
                "station_lat": 46.0824088609516
            }
        ]
        lt.station_producer = mock.Mock()
        res1 = {
                "station_ref_id": "103061",
                "scraped": "2017-03-21T00:00:00+00:00",
                "route_name": "GARA\u017dA",
                "station_lng": 14.5072916018955,
                "station_name": "Pohorskega bataljona",
                "route_num_sub": "",
                "station_direction": "\u2192",
                "station_int_id": 2211,
                "route_int_id": 1047,
                "route_num": 14,
                "station_lat": 46.0824088609516
            }
        res2 = {
                "station_ref_id": "103061",
                "scraped": "2017-03-21T00:00:00+00:00",
                "route_name": "BOKALCE",
                "station_lng": 14.5072916018955,
                "station_name": "Pohorskega bataljona",
                "route_num_sub": "",
                "station_direction": "\u2192",
                "station_int_id": 2211,
                "route_int_id": 987,
                "route_num": 14,
                "station_lat": 46.0824088609516
            }

        lt.run_station()

        self.assertEqual(lt.station_producer.send.call_count, 2)
        args1, kwargs1 = lt.station_producer.send.call_args_list[0]
        self.assertEqual(args1[0], res1)
        args2, kwargs2 = lt.station_producer.send.call_args_list[1]
        self.assertEqual(args2[0], res2)
        lt.station_producer.flush.assert_called_once()

if __name__ == '__main__':
    unittest.main()
