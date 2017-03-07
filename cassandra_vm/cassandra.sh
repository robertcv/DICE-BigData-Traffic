#!/bin/bash

#java
echo 'java installation'
sudo apt-get install -y python-software-properties debconf-utils > /dev/null
sudo add-apt-repository ppa:webupd8team/java -y 2> /dev/null
sudo apt-get update > /dev/null
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get install oracle-java8-installer -y &> /dev/null 

#make a folder for cassandra
mkdir cassandra
echo 'download cassandra'
#Download Cassandra
wget http://www.apache.si/cassandra/3.0.11/apache-cassandra-3.0.11-bin.tar.gz 2> /dev/null

echo 'extract cassandra archive'
#extract archive to cassandra folder
tar -xvf apache-cassandra-3.0.11-bin.tar.gz > /dev/null

mv apache-cassandra-3.0.11/* cassandra > /dev/null

rmdir apache-cassandra-3.0.11
rm apache-cassandra-3.0.11-bin.tar.gz
