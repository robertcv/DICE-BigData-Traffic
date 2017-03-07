#!/bin/bash

cd ~/confluent

bin/zookeeper-server-start etc/kafka/zookeeper.properties > /dev/null &
sleep 5
bin/kafka-server-start etc/kafka/server.properties > /dev/null &
sleep 5

export CLASSPATH=~/stream-reactor/libs/kafka-connect-cassandra-0.2.4-3.1.1-all.jar

cp  etc/schema-registry/connect-avro-distributed.properties etc/schema-registry/connect-distributed-json.properties

sed -i 's/io.confluent.connect.avro.AvroConverter/org.apache.kafka.connect.json.JsonConverter/g' etc/schema-registry/connect-distributed-json.properties
sed -i 's/schema.registry.url=http:\/\/localhost:8081/schemas.enable=false/g' etc/schema-registry/connect-distributed-json.properties

# nano etc/schema-registry/connect-distributed-json.properties
# 
# key.converter=org.apache.kafka.connect.json.JsonConverter
# key.converter.schemas.enable=false
# value.converter=org.apache.kafka.connect.json.JsonConverter
# value.converter.schemas.enable=false


bin/connect-distributed etc/schema-registry/connect-distributed-json.properties > /dev/null &
sleep 5 

cd ~/stream-reactor/

cp conf/cassandra-sink.properties conf/cassandra-sink.properties-orig

# nano conf/cassandra-sink.properties
# 
# connect.cassandra.contact.points=192.168.0.61

sed -i 's/localhost/192.168.0.61/g' conf/cassandra-sink.properties

bin/cli.sh create cassandra-sink-orders < conf/cassandra-sink.properties

