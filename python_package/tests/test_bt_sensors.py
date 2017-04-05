import unittest
import unittest.mock as mock

from pytraffic.collectors import bt_sensors


@mock.patch('pytraffic.collectors.bt_sensors.kafka_producer')
@mock.patch('pytraffic.collectors.bt_sensors.scraper')
@mock.patch('pytraffic.collectors.bt_sensors.files')
class BtSensorsTest(unittest.TestCase):
    conf = {
        'kafka_host': 'host',
        'bt_sensors': {
            'last_url': 'https://test.si/bt_sensors/velocities_avgs_last/',
            'sensors_url': 'https://test.si/bt_sensors/sensors/',
            'timon_username': 'username',
            'timon_password': 'password',
            'timon_crt_file': 'crt',
            'img_dir': 'img/',
            'data_file': 'data/bt_sensors.json',
            'data_age': 60 * 60 * 24,
            'not_lj': ['BTR0215'],
            'kafka_topic': 'bt_json'
        },
        'scraper': 'scraper'
    }

    def test_load_data(self, mock_f, mock_s, mock_k):
        bt = bt_sensors.BtSensors(self.conf)
        bt.get_web_data = mock.Mock()
        bt.get_local_data = mock.Mock()

        mock_f.old_or_not_exists.return_value = False
        bt.load_data()
        self.assertEqual(bt.get_web_data.call_count, 0)
        self.assertEqual(bt.get_local_data.call_count, 1)

        mock_f.old_or_not_exists.return_value = True
        bt.load_data()
        self.assertEqual(bt.get_web_data.call_count, 1)
        # just one call from before
        self.assertEqual(bt.get_local_data.call_count, 1)

    @mock.patch('builtins.open')
    @mock.patch('pytraffic.collectors.bt_sensors.json')
    def test_get_local_data(self, mock_json, mock_open, mock_f, mock_s, mock_k):
        mock_f.file_path.return_value = '~/data/bt_sensors.json'
        bt = bt_sensors.BtSensors(self.conf)
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_json.load.return_value = {'data': [1, 2, 3]}
        bt.get_local_data()
        mock_open.assert_called_once_with('~/data/bt_sensors.json')
        mock_json.load.assert_called_once_with(data_file)
        self.assertEqual(bt.sensors_data, [1, 2, 3])

    @mock.patch('builtins.open')
    @mock.patch('pytraffic.collectors.bt_sensors.json')
    def test_get_web_data(self, mock_json, mock_open, mock_f, mock_s, mock_k):
        mock_f.file_path.return_value = '~/data/bt_sensors.json'
        data_file = mock.Mock()
        mock_open.return_value.__enter__.return_value = data_file
        mock_s.Scraper.return_value.get_json.return_value = {'data': [1, 2, 3]}
        bt = bt_sensors.BtSensors(self.conf)
        bt.get_web_data()
        mock_open.assert_called_once_with('~/data/bt_sensors.json', 'w')
        mock_json.dump.assert_called_once_with({'data': [1, 2, 3]}, data_file)
        self.assertEqual(bt.sensors_data, [1, 2, 3])

        bt.get_local_data = mock.Mock()
        bt.w_scraper.get_json.return_value = None
        bt.get_web_data()
        self.assertEqual(bt.get_local_data.call_count, 1)

    def test_run(self, mock_f, mock_s, mock_k):
        mock_s.Scraper.return_value.get_json.return_value = {
            "totalPages": 1,
            "currentPage": 1,
            "totalElements": 28,
            "elementsPerPage": 100,
            "data": [
                {
                    "count": 1,
                    "avgSpeed": 44.643,
                    "timestampFrom": "2017-03-28T10:55:00+02:00",
                    "allCount": 1,
                    "toBtId": "BTR0206",
                    "fromBtId": "BTR0215",
                    "avgTravelTime": 0.112,
                    "timestampTo": "2017-03-28T11:10:00+02:00",
                    "id": "58da2a40c0a6834de258bfa6"
                },
                {
                    "count": 17,
                    "avgSpeed": 35.66241176470588,
                    "timestampFrom": "2017-03-28T11:15:00+02:00",
                    "allCount": 18,
                    "toBtId": "BTR0212",
                    "fromBtId": "BTR0202",
                    "avgTravelTime": 0.030294117647058826,
                    "timestampTo": "2017-03-28T11:30:00+02:00",
                    "id": "58da2ef0c0a6834de258c020"
                }
            ]
        }

        bt = bt_sensors.BtSensors(self.conf)
        bt.sensors_data = [
            {
                "neighbours": [
                    {
                        "distance": 500,
                        "btId": "BTR0201"
                    },
                    {
                        "distance": 1800,
                        "btId": "BTR0203"
                    },
                    {
                        "distance": 1010,
                        "btId": "BTR0212"
                    }
                ],
                "btId": "BTR0202",
                "id": "57531a9fbffebc11048b4567",
                "loc": {
                    "lng": 14.50978,
                    "lat": 46.06826
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 470,
                        "btId": "BTR0205"
                    },
                    {
                        "distance": 5000,
                        "btId": "BTR0215"
                    },
                    {
                        "distance": 2010,
                        "btId": "BTR0216"
                    }
                ],
                "btId": "BTR0206",
                "id": "57535b23bee8e3121ed7df95",
                "loc": {
                    "lng": 14.50072,
                    "lat": 46.04619
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 1010,
                        "btId": "BTR0202"
                    }
                ],
                "btId": "BTR0212",
                "id": "57535b23bee8e3121ed7df99",
                "loc": {
                    "lng": 14.49663,
                    "lat": 46.06703
                }
            }]

        res = {
            'toBtLng': 14.49663,
            'id': '58da2ef0c0a6834de258c020',
            'toBtLat': 46.06703,
            'avgTravelTime': 0.030294117647058826,
            'timestampTo': '2017-03-28T09:30:00Z',
            'timestampFrom': '2017-03-28T09:15:00Z',
            'fromBtId': 'BTR0202',
            'fromBtLng': 14.50978,
            'fromBtLat': 46.06826,
            'toBtId': 'BTR0212',
            'avgSpeed': 35.66241176470588,
            'count': 17,
            'allCount': 18,
            'distance': 1010
        }

        bt.run()
        mock_k.Producer.return_value.send.assert_called_once_with(res)

    def test_get_plot_data(self, mock_f, mock_s, mock_k):

        bt = bt_sensors.BtSensors(self.conf)
        bt.sensors_data = [
            {
                "neighbours": [
                    {
                        "distance": 500,
                        "btId": "BTR0201"
                    },
                    {
                        "distance": 1800,
                        "btId": "BTR0203"
                    },
                    {
                        "distance": 1010,
                        "btId": "BTR0212"
                    }
                ],
                "btId": "BTR0202",
                "id": "57531a9fbffebc11048b4567",
                "loc": {
                    "lng": 14.50978,
                    "lat": 46.06826
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 470,
                        "btId": "BTR0205"
                    },
                    {
                        "distance": 5000,
                        "btId": "BTR0215"
                    },
                    {
                        "distance": 2010,
                        "btId": "BTR0216"
                    }
                ],
                "btId": "BTR0206",
                "id": "57535b23bee8e3121ed7df95",
                "loc": {
                    "lng": 14.50072,
                    "lat": 46.04619
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 1010,
                        "btId": "BTR0202"
                    }
                ],
                "btId": "BTR0212",
                "id": "57535b23bee8e3121ed7df99",
                "loc": {
                    "lng": 14.49663,
                    "lat": 46.06703
                }
            },
            {
                "neighbours": [
                    {
                        "distance": 5000,
                        "btId": "BTR0206"
                    },
                    {
                        "distance": 4600,
                        "btId": "BTR0218"
                    }
                ],
                "btId": "BTR0215",
                "id": "57535b23bee8e3121ed7df9c",
                "loc": {
                    "lng": 14.54398,
                    "lat": 46.01633
                }
            }]

        lng, lat, labels = bt.get_plot_data()
        self.assertEqual(lng, [14.50978, 14.50072, 14.49663])
        self.assertEqual(lat, [46.06826, 46.04619, 46.06703])
        self.assertEqual(labels, ['BTR0202', 'BTR0206', 'BTR0212'])


if __name__ == '__main__':
    unittest.main()
