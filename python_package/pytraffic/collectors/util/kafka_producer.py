import json

from kafka import KafkaProducer
from kafka.errors import KafkaError
from pytraffic.collectors.util import exceptions


class Producer(object):
    """
    This class is a wrapper around the official kafka module.
    Its main purpose is to catch connection exceptions.
    """

    def __init__(self, kafka_host, topic):
        """
        Initialize Kafka connection.

        Args:
            kafka_host (str): Hostname and port for Kafka (host:port).
            topic (str): Name of topic to which data is send.

        """
        self.kafka_host = kafka_host
        self.connection = None
        self.topic = topic
        self.connection = self.connect()

    def connect(self):
        """
        Start a connection with Kafka.

        Returns:
            KafkaProducer object that is used to send data to Kafka.

        Raises:
            ConnectionError: If connection couldn't be established.
        """
        try:
            return KafkaProducer(bootstrap_servers=[self.kafka_host],
                                 value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                                 retries=5)
        except KafkaError:
            raise exceptions.ConnectionError(
                'Kafka on {}'.format(self.kafka_host))

    def send(self, data):
        """
        Send data to Kafka topic.

        Args:
            data (dict): Data to be send to Kafka.

        """
        self.connection.send(self.topic, data)

    def flush(self):
        """
        Makes all buffered records immediately available to send and blocks on
        the completion of the requests associated with these records.
        """
        self.connection.flush()
