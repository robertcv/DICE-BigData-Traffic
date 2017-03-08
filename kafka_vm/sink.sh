#!/bin/bash

cd ~/stream-reactor/
cp conf/cassandra-sink.properties conf/cassandra-sink-bt-sensors.properties

sed -i 's/cassandra-sink-orders/cs-bt-sensors/' conf/cassandra-sink-bt-sensors.properties
sed -i 's/orders-topic/bt_json/' conf/cassandra-sink-bt-sensors.properties
sed -i 's/orders/bt_sensors/' conf/cassandra-sink-bt-sensors.properties
sed -i 's/localhost/192.168.0.61/' conf/cassandra-sink-bt-sensors.properties
sed -i 's/demo/dice/' conf/cassandra-sink-bt-sensors.properties

bin/cli.sh create cs-bt-sensors < conf/cassandra-sink-bt-sensors.properties