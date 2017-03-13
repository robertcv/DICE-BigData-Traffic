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

bin/cli.sh create cs-bt-sensors < conf/cassandra-sink-bt-sensors.properties > /dev/null
sleep 5

# inductive loops
cp conf/cassandra-sink.properties conf/cassandra-sink-inductive-loops.properties

sed -i 's/cassandra-sink-orders/cs-inductive-loops/' conf/cassandra-sink-inductive-loops.properties
sed -i 's/orders-topic/inductive_json/' conf/cassandra-sink-inductive-loops.properties
sed -i 's/orders/inductive_loops/' conf/cassandra-sink-inductive-loops.properties

bin/cli.sh create cs-inductive-loops < conf/cassandra-sink-inductive-loops.properties > /dev/null
sleep 5

# counters
cp conf/cassandra-sink.properties conf/cassandra-sink-counters.properties

sed -i 's/cassandra-sink-orders/cs-counters/' conf/cassandra-sink-counters.properties
sed -i 's/orders-topic/counter_json/' conf/cassandra-sink-counters.properties
sed -i 's/orders/counters/' conf/cassandra-sink-counters.properties

bin/cli.sh create cs-counters < conf/cassandra-sink-counters.properties > /dev/null
sleep 5

# pollution
cp conf/cassandra-sink.properties conf/cassandra-sink-pollution.properties

sed -i 's/cassandra-sink-orders/cs-pollution/' conf/cassandra-sink-pollution.properties
sed -i 's/orders-topic/pollution_json/' conf/cassandra-sink-pollution.properties
sed -i 's/orders/pollution/' conf/cassandra-sink-pollution.properties

bin/cli.sh create cs-pollution < conf/cassandra-sink-pollution.properties > /dev/null
sleep 5

# lpp_station
cp conf/cassandra-sink.properties conf/cassandra-sink-lpp-station.properties

sed -i 's/cassandra-sink-orders/cs-lpp-station/' conf/cassandra-sink-lpp-station.properties
sed -i 's/orders-topic/lpp_station_json/' conf/cassandra-sink-lpp-station.properties
sed -i 's/orders/lpp_station/' conf/cassandra-sink-lpp-station.properties

bin/cli.sh create cs-lpp-station < conf/cassandra-sink-lpp-station.properties > /dev/null
sleep 5

# lpp_static
cp conf/cassandra-sink.properties conf/cassandra-sink-lpp-static.properties

sed -i 's/cassandra-sink-orders/cs-lpp-static/' conf/cassandra-sink-lpp-static.properties
sed -i 's/orders-topic/lpp_static_json/' conf/cassandra-sink-lpp-static.properties
sed -i 's/orders/lpp_static/' conf/cassandra-sink-lpp-static.properties

bin/cli.sh create cs-lpp-static < conf/cassandra-sink-lpp-static.properties > /dev/null
sleep 5

# lpp_live
cp conf/cassandra-sink.properties conf/cassandra-sink-lpp-live.properties

sed -i 's/cassandra-sink-orders/cs-lpp-live/' conf/cassandra-sink-lpp-live.properties
sed -i 's/orders-topic/lpp_live_json/' conf/cassandra-sink-lpp-live.properties
sed -i 's/orders/lpp_live/' conf/cassandra-sink-lpp-live.properties

bin/cli.sh create cs-lpp-live < conf/cassandra-sink-lpp-live.properties > /dev/null
sleep 5

cd ~/kafka
kill $(cat connect.pid)
export CLASSPATH=~/stream-reactor/libs/kafka-connect-cassandra-0.2.4-3.1.1-all.jar
bin/connect-distributed.sh config/connect-distributed.properties &> connect.log &
echo $! > connect.pid
sleep 5