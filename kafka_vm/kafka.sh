#!/bin/bash

echo 'java installation'
#java
sudo apt-get install -y python-software-properties debconf-utils > /dev/null
sudo add-apt-repository ppa:webupd8team/java -y 2> /dev/null
sudo apt-get update > /dev/null
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get install oracle-java8-installer -y &> /dev/null

#make kafka home folder
mkdir kafka

echo 'download kafka'
#download kafka
wget http://www.apache.si/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz 2> /dev/null

echo 'extract kafka archive'
#extract archive to kafka folder
tar -xzf kafka_2.11-0.10.2.0.tgz > /dev/null

mv kafka_2.11-0.10.2.0/* kafka > /dev/null

rm kafka_2.11-0.10.2.0.tgz
rmdir kafka_2.11-0.10.2.0/

#Stream reactor release 0.2.4
mkdir stream-reactor

echo 'download Stream reactor'
wget https://github.com/datamountaineer/stream-reactor/releases/download/v0.2.4/stream-reactor-0.2.4-3.1.1.tar.gz 2> /dev/null

echo 'extract confluent Stream reactor'
tar xvf stream-reactor-0.2.4-3.1.1.tar.gz > /dev/null

mv stream-reactor-0.2.4-3.1.1/* stream-reactor > /dev/null

rmdir stream-reactor-0.2.4-3.1.1
rm stream-reactor-0.2.4-3.1.1.tar.gz
