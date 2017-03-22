class CollectorError(Exception):
    """
    Base exception for collectors.
    """

    def __init__(self, conditions, msg):
        """
        Construct CollectorError exception.

        Args:
            conditions (str): More information on exception.
            msg (str): Message explaining reason for exception.

        """
        super(CollectorError, self).__init__(msg)
        self.conditions = conditions


class ConnectionError(CollectorError):
    """
    This exception is raised if connection was not successful.
    """

    def __init__(self, conditions):
        """
        Construct ConnectionError exception.

        Args:
            conditions (str): More information on exception.

        """
        msg = "Unable to connect to {}".format(conditions)
        super(ConnectionError, self).__init__(conditions, msg)


class StatusCodeError(CollectorError):
    """
    This exception is raised if we get a response code different from 200.
    """

    def __init__(self, conditions):
        """
        Construct StatusCodeError exception.

        Args:
            conditions (str): More information on exception.

        """
        msg = "Response with status code {}".format(conditions)
        super(StatusCodeError, self).__init__(conditions, msg)


class SearchError(CollectorError):
    """
    This exception is raised if search was not successful.
    """

    def __init__(self, conditions):
        """
        Construct SearchError exception.

        Args:
            conditions (str): More information on exception.

        """
        msg = "No search results for {}".format(conditions)
        super(SearchError, self).__init__(conditions, msg)
