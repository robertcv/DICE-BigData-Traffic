import requests
import sys

from time import sleep
from pytraffic import settings


class Scraper:
    def __init__(self, **kwargs):
        self.kwarg = kwargs
        self.sleep_sec = settings.SCRAPER_SLEEP
        self.ignore_status_code = settings.SCRAPER_IGNORE_STATUS_CODE
        self.retries = settings.SCRAPER_RETRIES
        self.last_status_code = None

        if 'timeout' not in self.kwarg:
            self.kwarg['timeout'] = settings.SCRAPER_TIMEOUT

        if 'ignore_status_code' in self.kwarg:
            self.ignore_status_code = self.kwarg['ignore_status_code']
            del self.kwarg['ignore_status_code']

        if 'retries' in self.kwarg:
            self.retries = self.kwarg['retries']
            del self.kwarg['retries']

        if 'sleep' in self.kwarg:
            self.sleep_sec = self.kwarg['sleep']
            del self.kwarg['sleep']

    def connect(self, url):
        retries = self.retries
        while retries > 0:
            try:
                response = requests.get(url, **self.kwarg)
                return response
            except:
                retries -= 1
                sleep(self.sleep_sec)
        else:
            sys.exit(1)

    def get_response(self, url):
        response = self.connect(url)

        self.last_status_code = response.status_code
        if self.last_status_code == 200:
            return response

        elif self.ignore_status_code:
            return None

        else:
            sys.exit(1)

    def get_json(self, url):
        response = self.get_response(url)
        if response is not None:
            return response.json()
        return None

    def get_text(self, url):
        response = self.get_response(url)
        if response is not None:
            return response.text
        return None
