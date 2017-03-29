import unittest

from pytraffic.collectors.util import date_time


class DateTimeTest(unittest.TestCase):

    def test_now_isoformat(self):

        re = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}'

        self.assertRegex(date_time.now_isoformat(), re)

    def test_today_timestamp(self):

        re = r'\d{13}'

        self.assertRegex(date_time.today_timestamp(), re)

if __name__ == '__main__':
    unittest.main()
