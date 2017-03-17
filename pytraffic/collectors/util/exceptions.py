class CollectorError(Exception):
    def __init__(self, conditions, msg):
        super(CollectorError, self).__init__(msg)
        self.conditions = conditions


class ConnectionError(CollectorError):
    def __init__(self, conditions):
        msg = "Unable to connect to {}".format(conditions)
        super(ConnectionError, self).__init__(conditions, msg)


class StatusCodeError(CollectorError):
    def __init__(self, conditions):
        msg = "Response with status code {}".format(conditions)
        super(StatusCodeError, self).__init__(conditions, msg)


class SearchError(CollectorError):
    def __init__(self, conditions):
        msg = "No search results for {}".format(conditions)
        super(SearchError, self).__init__(conditions, msg)
