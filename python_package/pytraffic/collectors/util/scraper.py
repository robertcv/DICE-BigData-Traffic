import requests

from time import sleep
from pytraffic import settings
from pytraffic.collectors.util import exceptions


class Scraper:
    """
    This class enables easy usage of request module. Its main feature is trying
    to connect multiple times before throwing an exception.
    """

    def __init__(self, ignore_status_code=None, retries=None, sleep_sec=None,
                 **kwargs):
        """
        This __init__ sets the necessary arguments for connecting with request.

        Args:
            ignore_status_code (bool, optional): Raise exception for status
                codes if not set.
            retries (int, optional): Number of connection retries before raising
                an exception.
            sleep_sec (int, optional): Number of seconds between retiring to
                connect.
            **kwargs: Request arguments.

        """
        self.kwarg = kwargs
        self.sleep_sec = settings.SCRAPER_SLEEP
        self.ignore_status_code = settings.SCRAPER_IGNORE_STATUS_CODE
        self.retries = settings.SCRAPER_RETRIES
        self.last_status_code = None
        self.last_exception = None

        if ignore_status_code is not None:
            self.ignore_status_code = ignore_status_code

        if retries is not None:
            self.retries = retries

        if sleep_sec is not None:
            self.sleep_sec = sleep_sec

        if 'timeout' not in self.kwarg:
            self.kwarg['timeout'] = settings.SCRAPER_TIMEOUT

    def connect(self, url):
        """
        Try to get a response from url. If there is an exception wait and try
        again. If after multiple we don successfully get a response raise
        exception.

        Args:
            url (str): Url to ger a response from.

        Raises:
            ConnectionError: If no response after multiple attempts.

        """
        retries = self.retries
        while retries > 0:
            try:
                response = requests.get(url, **self.kwarg)
                return response
            except Exception as e:
                self.last_exception = e
                retries -= 1
                sleep(self.sleep_sec)
        else:
            raise exceptions.ConnectionError(url)

    def get_response(self, url):
        """
        Try to get a response from url. The check for te response status code.
        If ignore_status_code is set to False the raise exception on code
        different from 200.

        Args:
            url (str): Url to ger a response from.

        Returns:
            :obj:`Response`: Response object or None.

        """
        response = self.connect(url)

        self.last_status_code = response.status_code
        if self.last_status_code == 200:
            return response

        elif self.ignore_status_code:
            return None

        else:
            raise exceptions.StatusCodeError(
                "{} from {}".format(self.last_status_code, url))

    def get_json(self, url):
        """
        Try to get a response from url. Return only the json part of the
        response.

        Args:
            url (str): Url to ger json data from.

        Returns:
            dict: Json data or None.

        """
        response = self.get_response(url)
        if response is not None:
            return response.json()
        return None

    def get_text(self, url):
        """
        Try to get a response from url. Return only the html as string.

        Args:
            url (str): Url to ger html from.

        Returns:
            str: Html code or None.

        """
        response = self.get_response(url)
        if response is not None:
            return response.text
        return None
