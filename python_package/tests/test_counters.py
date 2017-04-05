import unittest
import unittest.mock as mock

from pytraffic.collectors import counters


@mock.patch('pytraffic.collectors.counters.kafka_producer.Producer')
@mock.patch('pytraffic.collectors.counters.scraper.Scraper')
class TrafficCounterTest(unittest.TestCase):
    conf = {
        'kafka_host': 'host',
        'counters': {
            'url': 'https://test.si/promet/counters/',
            'img_dir': 'img/',
            'kafka_topic': 'counter_json'
        },
        'location': {
            'min_lng': 14.44,
            'max_lng': 14.58,
            'min_lat': 46.0,
            'max_lat': 46.1
        },
        'scraper': 'scraper'
    }

    def test_load_data(self, mock_s, mock_k):
        mock_s.return_value.get_json.return_value = {
            'Contents': [{'Data': {'Items': 'data'}}]}
        tc = counters.TrafficCounter(self.conf)
        self.assertEqual(tc.load_data(), 'data')

    def test_run(self, mock_s, mock_k):
        mock_s.return_value.get_json.return_value = {
            "RoutingVersion": 1,
            "updated": 1490700723,
            "TileVersion": 0,
            "ModifiedTime": "2017-03-28T11:30:18.9825629Z",
            "copyright": "Prometno-informacijski center za dr\u017eavne ceste",
            "ModelVersion": 1,
            "Expires": "2017-03-28T11:32:29.3695018Z",
            "Contents": [
                {
                    "Language": "sl_SI",
                    "ModifiedTime": "2017-03-28T11:30:18.9825629Z",
                    "IsModified": True,
                    "ContentName": "stevci",
                    "Expires": "2017-03-28T11:40:18.9825629Z",
                    "ETag": "5mZJiN2U8MojkjCTL6HH3DxWxBIzutq176rDLso9UE1UC2oTcuJRcnMgH7IlSubFGwzQP/rKP0bQg8PggmFlRA==",
                    "Data": {
                        "ContentName": "stevci",
                        "Language": "sl_SI",
                        "Items": [
                            {
                                "y_wgs": 46.0842126150332,
                                "Description": "HC-H3, LJ (S obvoznica)",
                                "Title": "HC-H3, LJ (S obvoznica)",
                                "ContentName": "stevci",
                                "x_wgs": 14.501172525698411,
                                "CrsId": "EPSG:2170",
                                "stevci_cestaOpis": "HC-H3",
                                "Y": 104571.0,
                                "X": 461802.0,
                                "Icon": "res/icons/stevci/stevec_3.png",
                                "Data": [
                                    {
                                        "properties": {
                                            "stevci_gap": "2,5",
                                            "stevci_statOpis": "Zgo\u0161\u010den promet",
                                            "stevci_hit": "95",
                                            "stevci_stev": "1212",
                                            "stevci_pasOpis": "(v)",
                                            "stevci_smerOpis": "LJ Savlje - LJ Dunajska",
                                            "stevci_stat": "3"
                                        },
                                        "Id": "0174-21",
                                        "Icon": "3"
                                    },
                                    {
                                        "properties": {
                                            "stevci_gap": "3,1",
                                            "stevci_statOpis": "Zgo\u0161\u010den promet",
                                            "stevci_hit": "119",
                                            "stevci_stev": "1056",
                                            "stevci_pasOpis": "(p)",
                                            "stevci_smerOpis": "LJ Savlje - LJ Dunajska",
                                            "stevci_stat": "3"
                                        },
                                        "Id": "0174-22",
                                        "Icon": "3"
                                    }
                                ],
                                "Id": "0174",
                                "stevci_lokacijaOpis": "LJ (S obvoznica)"
                            },
                            {
                                "y_wgs": 46.252158103340356,
                                "Description": "R3-752, Ljube\u010dna",
                                "Title": "R3-752, Ljube\u010dna",
                                "ContentName": "stevci",
                                "x_wgs": 15.3107103763711,
                                "CrsId": "EPSG:2170",
                                "stevci_cestaOpis": "R3-752",
                                "Y": 123164.0,
                                "X": 524337.0,
                                "Icon": "res/icons/stevci/stevec_1.png",
                                "Data": [
                                    {
                                        "properties": {
                                            "stevci_gap": "16,4",
                                            "stevci_statOpis": "Normalen promet",
                                            "stevci_hit": "58",
                                            "stevci_stev": "180",
                                            "stevci_pasOpis": "",
                                            "stevci_smerOpis": "AC - Celje",
                                            "stevci_stat": "1"
                                        },
                                        "Id": "0694-11",
                                        "Icon": "1"
                                    },
                                    {
                                        "properties": {
                                            "stevci_gap": "14,6",
                                            "stevci_statOpis": "Normalen promet",
                                            "stevci_hit": "58",
                                            "stevci_stev": "264",
                                            "stevci_pasOpis": "",
                                            "stevci_smerOpis": "Celje - AC",
                                            "stevci_stat": "1"
                                        },
                                        "Id": "0694-21",
                                        "Icon": "1"
                                    }
                                ],
                                "Id": "0694",
                                "stevci_lokacijaOpis": "Ljube\u010dna"
                            }
                        ]
                    }
                }
            ]
        }
        tc = counters.TrafficCounter(self.conf)
        res1 = {
            'stevci_hit': 95,
            'y_wgs': 46.0842126150332,
            'Icon': 'res/icons/stevci/stevec_3.png',
            'stevci_stat': 3,
            'modified': '2017-03-28T11:30:18.982Z',
            'Y': 104571.0,
            'stevci_smerOpis': 'LJ Savlje - LJ Dunajska',
            'id': '0174-21',
            'stevci_pasOpis': '(v)',
            'ContentName': 'stevci', 'stevci_stev': 1212, 'CrsId': 'EPSG:2170',
            'Title': 'HC-H3, LJ (S obvoznica)', 'Id': '0174',
            'x_wgs': 14.501172525698411,
            'stevci_lokacijaOpis': 'LJ (S obvoznica)',
            'stevci_cestaOpis': 'HC-H3',
            'Description': 'HC-H3, LJ (S obvoznica)',
            'stevci_statOpis': 'Zgoščen promet', 'stevci_gap': 2.5,
            'X': 461802.0
        }

        res2 = {
            'stevci_hit': 119, 'y_wgs': 46.0842126150332,
            'Icon': 'res/icons/stevci/stevec_3.png', 'stevci_stat': 3,
            'modified': '2017-03-28T11:30:18.982Z', 'Y': 104571.0,
            'stevci_smerOpis': 'LJ Savlje - LJ Dunajska', 'id': '0174-22',
            'stevci_pasOpis': '(p)', 'ContentName': 'stevci',
            'stevci_stev': 1056, 'CrsId': 'EPSG:2170',
            'Title': 'HC-H3, LJ (S obvoznica)', 'Id': '0174',
            'x_wgs': 14.501172525698411,
            'stevci_lokacijaOpis': 'LJ (S obvoznica)',
            'stevci_cestaOpis': 'HC-H3',
            'Description': 'HC-H3, LJ (S obvoznica)',
            'stevci_statOpis': 'Zgoščen promet', 'stevci_gap': 3.1,
            'X': 461802.0
        }
        tc.run()
        self.assertEqual(mock_k.return_value.send.call_count, 2)
        call = mock_k.return_value.send.call_args_list
        args1, kwargs1 = call[0]
        args2, kwargs2 = call[1]
        self.assertEqual(args1[0], res1)
        self.assertEqual(args2[0], res2)

    def test_get_plot_data(self, mock_s, mock_k):
        tc = counters.TrafficCounter(self.conf)
        tc.load_data = mock.Mock()
        tc.load_data.return_value = [
            {
                "y_wgs": 46.0842126150332,
                "Description": "HC-H3, LJ (S obvoznica)",
                "Title": "HC-H3, LJ (S obvoznica)",
                "ContentName": "stevci",
                "x_wgs": 14.501172525698411,
                "CrsId": "EPSG:2170",
                "stevci_cestaOpis": "HC-H3",
                "Y": 104571.0,
                "X": 461802.0,
                "Icon": "res/icons/stevci/stevec_3.png",
                "Data": [
                    {
                        "properties": {
                            "stevci_gap": "2,5",
                            "stevci_statOpis": "Zgo\u0161\u010den promet",
                            "stevci_hit": "95",
                            "stevci_stev": "1212",
                            "stevci_pasOpis": "(v)",
                            "stevci_smerOpis": "LJ Savlje - LJ Dunajska",
                            "stevci_stat": "3"
                        },
                        "Id": "0174-21",
                        "Icon": "3"
                    },
                    {
                        "properties": {
                            "stevci_gap": "3,1",
                            "stevci_statOpis": "Zgo\u0161\u010den promet",
                            "stevci_hit": "119",
                            "stevci_stev": "1056",
                            "stevci_pasOpis": "(p)",
                            "stevci_smerOpis": "LJ Savlje - LJ Dunajska",
                            "stevci_stat": "3"
                        },
                        "Id": "0174-22",
                        "Icon": "3"
                    }
                ],
                "Id": "0174",
                "stevci_lokacijaOpis": "LJ (S obvoznica)"
            },
            {
                "y_wgs": 46.252158103340356,
                "Description": "R3-752, Ljube\u010dna",
                "Title": "R3-752, Ljube\u010dna",
                "ContentName": "stevci",
                "x_wgs": 15.3107103763711,
                "CrsId": "EPSG:2170",
                "stevci_cestaOpis": "R3-752",
                "Y": 123164.0,
                "X": 524337.0,
                "Icon": "res/icons/stevci/stevec_1.png",
                "Data": [
                    {
                        "properties": {
                            "stevci_gap": "16,4",
                            "stevci_statOpis": "Normalen promet",
                            "stevci_hit": "58",
                            "stevci_stev": "180",
                            "stevci_pasOpis": "",
                            "stevci_smerOpis": "AC - Celje",
                            "stevci_stat": "1"
                        },
                        "Id": "0694-11",
                        "Icon": "1"
                    },
                    {
                        "properties": {
                            "stevci_gap": "14,6",
                            "stevci_statOpis": "Normalen promet",
                            "stevci_hit": "58",
                            "stevci_stev": "264",
                            "stevci_pasOpis": "",
                            "stevci_smerOpis": "Celje - AC",
                            "stevci_stat": "1"
                        },
                        "Id": "0694-21",
                        "Icon": "1"
                    }
                ],
                "Id": "0694",
                "stevci_lokacijaOpis": "Ljube\u010dna"
            }
        ]

        lng, lat = tc.get_plot_data()
        self.assertEqual(tc.load_data.call_count, 1)
        self.assertEqual(lng, [14.501172525698411])
        self.assertEqual(lat, [46.0842126150332])


if __name__ == '__main__':
    unittest.main()
