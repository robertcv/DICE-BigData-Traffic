import unittest

from pytraffic.collectors.util import date_time


class DateTimeTest(unittest.TestCase):

    def test_now_isoformat(self):

        re = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00Z'

        self.assertRegex(date_time.now_isoformat(), re)

    def test_today_timestamp(self):

        re = r'\d{13}'

        self.assertRegex(date_time.today_timestamp(), re)

    def test_hour_minut_to_utc(self):

        re = r'\d{4}-\d{2}-\d{2}T06:45:00Z'

        self.assertRegex(date_time.hour_minut_to_utc(8, 45), re)

    def test_local_to_utc(self):

        res = '2017-04-03T11:23:00Z'
        test = '2017-04-03T13:23:00.000Z' # the Z should be for utc but it isn't

        self.assertEqual(date_time.local_to_utc(test), res)

    def test_isoformat_to_utc(self):

        res = '2017-04-03T11:23:00Z'
        test = '2017-04-03T13:23:00+02:00'

        self.assertEqual(date_time.isoformat_to_utc(test), res)

if __name__ == '__main__':
    unittest.main()
