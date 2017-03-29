import unittest
import unittest.mock as mock

from pytraffic.collectors import inductive_loops


@mock.patch('pytraffic.collectors.inductive_loops.InductiveLoops.__init__',
            mock.Mock(return_value=None))
class InductiveLoopsTest(unittest.TestCase):
    def test_run(self):
        il = inductive_loops.InductiveLoops()
        il.ess = mock.Mock()
        il.ess.get_json.return_value = {
            "hits": {
                "hits": [
                    {
                        "_index": "inductive_loops",
                        "_source": {
                            "vmax": 50,
                            "numberOfVehicles": 444,
                            "deviceX": "46,055980",
                            "direction": 11,
                            "laneDescription": "(r)",
                            "title": "-, Zaloška cesta : Toplarniška ul. - Pot na Fužine (r)",
                            "stat": 1,
                            "id": "1010-11",
                            "point": "46,055980 14,545549",
                            "roadDescription": "-",
                            "occ": 67,
                            "date": "28/03/2017",
                            "region": "Ljubljana",
                            "updated": "2017-03-28T12:00:00Z",
                            "location": 1010,
                            "gap": 7.7,
                            "pkgdate": "2017-03-28T12:00:19Z",
                            "locationDescription": "Zaloška cesta",
                            "deviceY": "14,545549",
                            "time": "14:00:00",
                            "StatusDescription": "Normal traffic",
                            "avgSpeed": 57,
                            "roadSection": "-",
                            "chainage": 0,
                            "directionDescription": "Toplarniška ul. - Pot na Fužine",
                            "summary": "-, Zaloška cesta : Toplarniška ul. - Pot na Fužine (r) - Normal traffic (444 vehicles/h, avg. speed=57km/h, avg. gap=7.7s, occupancy=6.7%)"
                        },
                        "_id": "AVsUynl-BuZhfdcBSLNy",
                        "_type": "il_avg_velocity",
                        "_score": 1.0
                    }
                ],
                "total": 32,
                "max_score": 1.0
            },
            "took": 93,
            "_shards": {
                "successful": 5,
                "total": 5,
                "failed": 0
            },
            "timed_out": False
        }

        kafka_search_body = {
            "size": 10000,
            "query": {
                "bool": {
                    'must': [
                        {"range": {"updated": {"gte": "now-15m"}}}
                    ]
                }
            }
        }

        res = {
            'deviceX': 46.05598, 'pkgdate': '2017-03-28T12:00:19Z',
            'location': 1010,
            'directionDescription': 'Toplarniška ul. - Pot na Fužine',
            'direction': 11, 'time': '14:00:00', 'numberOfVehicles': 444,
            'laneDescription': '(r)', 'chainage': 0, 'gap': 7.7,
            'id': '1010-11', 'occ': 67, 'stat': 1, 'vmax': 50,
            'point': '46,055980 14,545549', 'region': 'Ljubljana',
            'deviceY': 14.545549, 'roadSection': '-', 'avgSpeed': 57,
            'updated': '2017-03-28T12:00:00Z',
            'title': '-, Zaloška cesta : Toplarniška ul. - Pot na Fužine (r)',
            'roadDescription': '-', 'StatusDescription': 'Normal traffic',
            'locationDescription': 'Zaloška cesta', 'date': '28/03/2017'
        }
        il.producer = mock.Mock()
        il.run()
        il.ess.get_json.assert_called_once_with(kafka_search_body)
        il.producer.send.assert_called_once_with(res)

    @mock.patch('pytraffic.collectors.inductive_loops.plot')
    def test_plot(self, mock_plot):
        il = inductive_loops.InductiveLoops()
        il.ess = mock.Mock()
        il.ess.get_json.return_value = {
            "hits": {
                "hits": [
                    {
                        "_index": "inductive_loops",
                        "_score": None,
                        "fields": {
                            "locationDescription": [
                                "Zaloška cesta"
                            ],
                            "updated": [
                                "2017-03-28T11:25:00Z"
                            ],
                            "location": [
                                1010
                            ],
                            "point": [
                                "46,055980 14,545549"
                            ]
                        },
                        "sort": [
                            1490700300000
                        ],
                        "_id": "AVsUriYYBuZhfdcBSKWR",
                        "_type": "il_avg_velocity"
                    },
                    {
                        "_index": "inductive_loops",
                        "_score": None,
                        "fields": {
                            "locationDescription": [
                                "Zaloška cesta"
                            ],
                            "updated": [
                                "2017-03-28T11:25:00Z"
                            ],
                            "location": [
                                1010
                            ],
                            "point": [
                                "46,055980 14,545549"
                            ]
                        },
                        "sort": [
                            1490700300000
                        ],
                        "_id": "AVsUriYiBuZhfdcBSKWS",
                        "_type": "il_avg_velocity"
                    },
                    {
                        "_index": "inductive_loops",
                        "_score": None,
                        "fields": {
                            "locationDescription": [
                                "Celovška cesta"
                            ],
                            "updated": [
                                "2017-03-28T11:25:00Z"
                            ],
                            "location": [
                                18
                            ],
                            "point": [
                                "46,057694 14,500324"
                            ]
                        },
                        "sort": [
                            1490700300000
                        ],
                        "_id": "AVsUriZQBuZhfdcBSKWX",
                        "_type": "il_avg_velocity"
                    }
                ],
                "total": 318,
                "max_score": None
            },
            "took": 117,
            "_shards": {
                "successful": 5,
                "total": 5,
                "failed": 0
            },
            "timed_out": False
        }

        map_search_body = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": [
                        {"range": {"updated": {"gte": "now-1h"}}}
                    ]
                }
            },
            "fields": ["point", "locationDescription", "updated", "location", ],
            "sort": [
                {"updated": "asc"}
            ]
        }

        il.plot_map('title', (10, 10), 100, 15, 5, (0.1, 0.2), 10, 'image.png')

        il.ess.get_json.assert_called_once_with(map_search_body)
        mock_plot.PlotOnMap.assert_called_once_with(
            [14.545549, 14.500324], [46.05598, 46.057694], 'title')
        mock_plot.PlotOnMap().generate.assert_called_once_with(
            (10, 10), 100, 15, 5)
        mock_plot.PlotOnMap().label.assert_called_once_with(
            [1010, 18], (0.1, 0.2), 10)
        mock_plot.PlotOnMap().save.assert_called_once_with(None, 'image.png')


if __name__ == '__main__':
    unittest.main()
