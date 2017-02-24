#!/bin/sh

sudo apt-get update
sudo apt-get install openjdk-7-jre -y

wget http://www.apache.si/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz
tar -xzf kafka_2.11-0.10.2.0.tgz
cd kafka_2.11-0.10.2.0/
