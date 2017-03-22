import json

from kafka import KafkaProducer
from kafka.errors import KafkaError
from pytraffic import settings
from pytraffic.collectors.util import exceptions


class Producer():
    """
    This class is a wrapper around the official kafka module.
    Its main purpose is to catch connection exceptions.
    """
    def __init__(self, topic):
        """
        Initialize Kafka connection.

        Args:
            topic (str): Name of topic to which data is send.

        """
        self.kafka_url = settings.KAFKA_HOST + ':' + settings.KAFKA_PORT
        self.connection = None
        self.topic = topic
        self.connect()

    def connect(self):
        """
        Start a connection with Kafka.

        Raises:
            ConnectionError: If connection couldn't be established.
        """
        try:
            self.connection = KafkaProducer(bootstrap_servers=[self.kafka_url],
                                            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                                            retries=5)
        except KafkaError:
            raise exceptions.ConnectionError('Kafka on {}'.format(self.kafka_url))

    def send(self, data):
        """
        Send data to Kafka topic.

        Args:
            data (dict): Data to be send to Kafka.

        Raises:
            ConnectionError: If it was not possible to send data.

        """
        try:
            future = self.connection.send(self.topic, data)
        except KafkaError:
            raise exceptions.ConnectionError('Kafka topic {}'.format(self.topic))

    def flush(self):
        """
        Makes all buffered records immediately available to send and blocks on
        the completion of the requests associated with these records.
        """
        self.connection.flush()
