from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

import datetime
import sys

"""
This Spark app takes counters and inductive loops data from Cassandra,
transforms and uses it to train a classifier to predict traffic data for the
next day.

Args:
    #1: Datetime in iso format from which the program should forecast traffic
        data.
    #2: Datetime in iso format to which the program should forecast traffic
        data.

Example:

    $ spark-submit \
    --packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.0-M3 \
    --conf spark.cassandra.connection.host=127.0.0.2 \
    --master spark://127.0.0.1:7077 \
    traffic_forecast.py 2017-05-04T00:00:00Z 2017-05-05T00:00:00Z

"""

spark = SparkSession.builder \
    .appName("TrafficForecast") \
    .getOrCreate()

# get data from cassandra
counters = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="counters", keyspace="dice")

il = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="inductive_loops", keyspace="dice")

tmp_counters = counters.select(
    'id',
    col('stevci_stat').alias('stat'),
    col('modified').alias('datetime'))

tmp_il = il.where('stat!=0').select(
    'id',
    'stat',
    col('updated').alias('datetime'))

traffic = tmp_counters.union(tmp_il)

# transform data
quarterTokens = udf(
    lambda time: float(time.hour * 4 + time.minute / 15), DoubleType())
traffic = traffic.withColumn('quarter', quarterTokens(traffic.datetime))

weekdayTokens = udf(lambda time: float(time.weekday()), DoubleType())
traffic = traffic.withColumn('weekday', weekdayTokens(traffic.datetime))

traffic = traffic.withColumn('stat_double', traffic['stat'].cast("double"))

idIndexer = StringIndexer(inputCol="id", outputCol="id_double").fit(traffic)
traffic = idIndexer.transform(traffic)

assembler = VectorAssembler(
    inputCols=['quarter', 'weekday', 'id_double'],
    outputCol='features')
data = assembler.transform(traffic)

# train random forrest classifier
dt = RandomForestClassifier(maxDepth=30, maxBins=100, minInstancesPerNode=20,
                            maxMemoryInMB=4048, labelCol="stat_double")
model = dt.fit(data)


# prepare data points for prediction
def datetime_range(start, end, step=15):
    cur = start
    while cur < end:
        quarter = cur.hour * 4 + cur.minute / 15
        weekday = cur.weekday()
        yield quarter, weekday, cur
        cur += datetime.timedelta(minutes=step)


ids_df = traffic.select('id').distinct().collect()
ids = [i.id for i in ids_df]

start = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%dT%H:%M:%SZ")
end = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%dT%H:%M:%SZ")

data = []
for q, w, dt in datetime_range(start, end):
    for i in ids:
        data.append((i, q, w, dt))

forecast_df = spark \
    .createDataFrame(data, ["id", "quarter", "weekday", "datetime"])

forecast_df = idIndexer.transform(forecast_df)
forecast_df = assembler.transform(forecast_df)

# forecast traffic
forecast_df = model.transform(forecast_df)

forecast_df = forecast_df.select(
    'id',
    col('prediction').alias('stat'),
    'datetime')

# save data back to cassandra
forecast_df.write \
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table="traffic_forecast", keyspace="dice_results") \
    .save()
