from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['192.168.0.62:9092'])

# Asynchronous by default
future = producer.send('test', b'to je iz pythona 2')

# Block for 'synchronous' sends
record_metadata = future.get(timeout=10)

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)