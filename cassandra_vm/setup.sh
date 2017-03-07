#!/bin/bash

cd ~/cassandra

sed -i 's/rpc_address: localhost/rpc_address: 192.168.0.61/' conf/cassandra.yaml

bin/cassandra

