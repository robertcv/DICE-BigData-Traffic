import unittest
import unittest.mock as mock

from pytraffic.collectors.util import kafka_producer


class KafkaProducerTest(unittest.TestCase):
    def setUp(self):
        self.mock_kafka = mock.Mock()
        kafka_producer.KafkaProducer = self.mock_kafka
        self.kafka = kafka_producer.Producer('127.0.0.1:9092', 'topic')

    def test_connect(self):
        args, kwargs = self.mock_kafka.call_args
        self.assertIn('127.0.0.1:9092', kwargs['bootstrap_servers'])

    def test_send(self):
        self.kafka.send({'data': [1, 2, 3]})
        self.mock_kafka.return_value.send.assert_called_once_with('topic', {
            'data': [1, 2, 3]})

    def test_flush(self):
        self.kafka.flush()
        self.mock_kafka.return_value.flush.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
