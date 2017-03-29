import unittest
import unittest.mock as mock

from pytraffic.collectors.util import kafka_producer


@mock.patch('pytraffic.collectors.util.kafka_producer.KafkaProducer')
class KafkaProducerTest(unittest.TestCase):
    def test_connect(self, mock_kafka):
        kafka_producer.Producer('topic')
        args, kwargs = mock_kafka.call_args
        self.assertIn('host:port', kwargs['bootstrap_servers'])

    def test_send(self, mock_kafka):
        kafka = kafka_producer.Producer('topic')
        kafka.send({'data': []})
        mock_kafka().send.assert_called_once_with('topic', {'data': []})

    def test_flush(self, mock_kafka):
        kafka = kafka_producer.Producer('topic')
        kafka.flush()
        mock_kafka().flush.assert_called_once()

if __name__ == '__main__':
    unittest.main()
