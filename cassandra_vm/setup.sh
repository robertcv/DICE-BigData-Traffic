#!/bin/bash

cd ~/cassandra

sed -i 's/rpc_address: localhost/rpc_address: 0.0.0.0/' conf/cassandra.yaml
sed -i 's/# broadcast_rpc_address: 1.2.3.4/broadcast_rpc_address: 192.168.0.61/' conf/cassandra.yaml

bin/cassandra &> cassandra.log
echo $! > cassandra.pid
sleep 5

bin/cqlsh -f ../tables.cql