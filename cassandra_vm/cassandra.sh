#!/bin/sh

#make confluent home folder
mkdir confluent

#download confluent
wget http://packages.confluent.io/archive/3.1/confluent-3.1.1-2.11.tar.gz

#extract archive to confluent folder
tar -xvf confluent-3.1.1-2.11.tar.gz -C confluent

#setup variables
export CONFLUENT_HOME=~/confluent/confluent-3.1.1

#make a folder for cassandra
mkdir cassandra

#Download Cassandra
wget http://apache.cs.uu.nl/cassandra/3.5/apache-cassandra-3.5-bin.tar.gz

#extract archive to cassandra folder
tar -xvf apache-cassandra-3.5-bin.tar.gz -C cassandra

#Set up environment variables
export CASSANDRA_HOME=~/cassandra/apache-cassandra-3.5-bin
export PATH=$PATH:$CASSANDRA_HOME/bin

#Start Cassandra
sudo sh ~/cassandra/bin/cassandra
