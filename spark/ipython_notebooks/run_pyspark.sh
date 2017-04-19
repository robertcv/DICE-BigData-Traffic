#!/bin/bash

PYSPARK_DRIVER_PYTHON=ipython2 \
PYSPARK_DRIVER_PYTHON_OPTS="notebook --ip=* --port=12345 --no-browser" \
$SPARK_HOME/bin/pyspark \
--packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.0-M3 \
--conf spark.cassandra.connection.host=10.10.43.76 \
--master local[6] --executor-memory 8GB