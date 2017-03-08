#!/bin/bash

cd ~/cassandra

sed -i 's/rpc_address: localhost/rpc_address: 0.0.0.0/' conf/cassandra.yaml
sed -i 's/# broadcast_rpc_address: 1.2.3.4/broadcast_rpc_address: 192.168.0.61/' conf/cassandra.yaml

bin/cassandra

#bin/cqlsh 192.168.0.61
#
#CREATE KEYSPACE lpp WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
#use lpp;
#
#create table lpp_live (station_int_id int, route_int_id int, arrival_time varchar, PRIMARY KEY (station_int_id, route_int_id));