#!/bin/bash

cd ~/stream-reactor/
cp conf/cassandra-sink.properties conf/cassandra-sink.properties-orig

sed -i 's/localhost/192.168.0.61/' conf/cassandra-sink.properties
sed -i 's/demo/dice/' conf/cassandra-sink.properties

# bt sensors
cp conf/cassandra-sink.properties conf/cassandra-sink-bt-sensors.properties

sed -i 's/cassandra-sink-orders/cs-bt-sensors/' conf/cassandra-sink-bt-sensors.properties
sed -i 's/orders-topic/bt_json/' conf/cassandra-sink-bt-sensors.properties
sed -i 's/orders/bt_sensors/' conf/cassandra-sink-bt-sensors.properties

bin/cli.sh create cs-bt-sensors < conf/cassandra-sink-bt-sensors.properties

# inductive loops
cp conf/cassandra-sink.properties conf/cassandra-sink-inductive-loops.properties

sed -i 's/cassandra-sink-orders/cs-inductive-loops/' conf/cassandra-sink-inductive-loops.properties
sed -i 's/orders-topic/inductive_json/' conf/cassandra-sink-inductive-loops.properties
sed -i 's/orders/inductive_loops/' conf/cassandra-sink-inductive-loops.properties

bin/cli.sh create cs-inductive-loops < conf/cassandra-sink-inductive-loops.properties

# counters
cp conf/cassandra-sink.properties conf/cassandra-sink-counters.properties

sed -i 's/cassandra-sink-orders/cs-counters/' conf/cassandra-sink-counters.properties
sed -i 's/orders-topic/counter_json/' conf/cassandra-sink-counters.properties
sed -i 's/orders/counters/' conf/cassandra-sink-counters.properties

bin/cli.sh create cs-counters < conf/cassandra-sink-counters.properties

