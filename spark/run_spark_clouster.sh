#!/bin/bash

spark-submit \
--packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.0-M3 \
--conf spark.cassandra.connection.host=10.10.43.76 \
--master $1 --executor-memory 2GB $2