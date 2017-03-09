#!/bin/bash

cd ~/kafka

bin/zookeeper-server-start.sh config/zookeeper.properties &> zoo.log &
sleep 5
bin/kafka-server-start.sh config/server.properties &> kafka.log &
sleep 5

export CLASSPATH=~/stream-reactor/libs/kafka-connect-cassandra-0.2.4-3.1.1-all.jar

sed -i 's/schemas.enable=true/schemas.enable=false/g' config/connect-distributed.properties

bin/connect-distributed.sh config/connect-distributed.properties &> connect.log &
sleep 5


