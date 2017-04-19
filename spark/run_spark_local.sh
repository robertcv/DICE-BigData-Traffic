#!/bin/bash

$SPARK_HOME/bin/spark-submit \
--packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.0-M3 \
--conf spark.cassandra.connection.host=10.10.43.76 \
--master local[6] --executor-memory 8GB $1