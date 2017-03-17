import json

from kafka import KafkaProducer
from kafka.errors import KafkaError
from pytraffic import settings
from pytraffic.collectors.util import exceptions


class Producer():
    def __init__(self, topic):
        self.kafka_url = settings.KAFKA_HOST + ':' + settings.KAFKA_PORT
        self.connection = None
        self.topic = topic
        self.connect()

    def connect(self):
        try:
            self.connection = KafkaProducer(bootstrap_servers=[self.kafka_url],
                                            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                                            retries=5)
        except KafkaError:
            raise exceptions.ConnectionError('Kafka on {}'.format(self.kafka_url))

    def send(self, data):
        try:
            future = self.connection.send(self.topic, data)
        except KafkaError:
            raise exceptions.ConnectionError('Kafka topic {}'.format(self.topic))

    def flush(self):
        self.connection.flush()
