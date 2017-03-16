import json
import sys

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
from pytraffic import settings


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
            sys.exit(1)

    def send(self, data):
        try:
            future = self.connection.send(self.topic, data)
        except KafkaTimeoutError:
            sys.exit(1)

    def flush(self):
        self.connection.flush()
