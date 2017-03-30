import requests

from time import sleep
from pytraffic.collectors.util import exceptions


class Scraper:
    """
    This class enables easy usage of request module. Its main feature is trying
    to connect multiple times before throwing an exception.
    """

    def __init__(self, conf, **kwargs):
        """
        This __init__ sets the necessary arguments for connecting with request.

        Args:
            conf (dict): This dict contains scraper configuration.
            **kwargs: Request arguments.

        """
        self.conf = conf
        self.kwarg = kwargs
        self.last_status_code = None
        self.last_exception = None

        if 'timeout' not in self.kwarg:
            self.kwarg['timeout'] = self.conf['timeout']

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
        retries = self.conf['retries']
        while retries > 0:
            try:
                response = requests.get(url, **self.kwarg)
                return response
            except Exception as e:
                self.last_exception = e
                retries -= 1
                sleep(self.conf['sleep'])
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

        elif self.conf['ignore_status_code']:
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
