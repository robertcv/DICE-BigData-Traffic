import unittest
import unittest.mock as mock

from pytraffic.collectors.util import scraper, exceptions


@mock.patch('pytraffic.collectors.util.scraper.requests')
class ScraperTest(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            'auth': ('username', 'password'),
            'verify': '/path/file.crt'
        }
        conf = {
            'timeout': 0.5,
            'retries': 3,
            'sleep': 0,
            'ignore_status_code': False
        }
        self.s = scraper.Scraper(conf, **self.kwargs)

        mock_obj = mock.MagicMock(status_code=200, text='<html></html>')
        mock_obj.json.return_value = {'data': [1,2,3]}
        self.mock_res = mock_obj

    def test_scraper(self, mock_r):
        self.assertEqual(self.s.kwarg['timeout'], 0.5)

    def test_connect(self, mock_r):
        mock_r.get.side_effect = [Exception(), Exception(), Exception(),
                                  self.mock_res]
        self.assertRaises(exceptions.ConnectionError, self.s.connect,
                          'http://test.com')
        self.assertEqual(mock_r.get.call_count, 3)
        self.kwargs['timeout'] = 0.5
        mock_r.get.assert_called_with('http://test.com', **self.kwargs)

        response = self.s.connect('http://test.com')
        self.assertEqual(response, self.mock_res)

    def test_response(self, mock_r):
        mock_r.get.return_value = self.mock_res
        response = self.s.get_response('http://test.com')
        self.assertEqual(response, self.mock_res)

        mock_r.get.return_value = mock.MagicMock(status_code=404)
        self.assertRaises(exceptions.StatusCodeError, self.s.get_response,
                          'http://test.com')

        self.s.conf['ignore_status_code'] = True
        response = self.s.get_response('http://test.com')
        self.assertEqual(response, None)

    def test_get_json(self, mock_r):
        mock_r.get.return_value = self.mock_res
        json = self.s.get_json('http://test.com')
        self.assertEqual(json, {'data': [1,2,3]})
        self.s.conf['ignore_status_code'] = True
        mock_r.get.return_value = mock.MagicMock(status_code=404)
        json = self.s.get_json('http://test.com')
        self.assertIsNone(json)

    def test_get_text(self, mock_r):
        mock_r.get.return_value = self.mock_res
        html = self.s.get_text('http://test.com')
        self.assertEqual(html, '<html></html>')
        self.s.conf['ignore_status_code'] = True
        mock_r.get.return_value = mock.MagicMock(status_code=404)
        html = self.s.get_text('http://test.com')
        self.assertIsNone(html)

if __name__ == '__main__':
    unittest.main()
