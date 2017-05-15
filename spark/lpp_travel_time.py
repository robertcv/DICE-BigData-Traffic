from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, lead, count, avg
from pyspark.sql.types import IntegerType
from pyspark.sql.window import Window

"""
This Spark app takes lpp buses arrival times from Cassandra and calculates
average travel time between two bus stations for every bus for every hour and
day of the week. This data is then saved back to Cassandra.
"""

spark = SparkSession.builder \
    .appName("LppTravelTime") \
    .getOrCreate()

lpp_live = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="lpp_live", keyspace="dice")

lpp_station_order = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="lpp_station_order", keyspace="dice_results")

# join to get stations order numbers
lpp = lpp_live.join(lpp_station_order, ['station_int_id', 'route_int_id'])

# create a window for adding columns with data from one row ahead
window = Window\
    .partitionBy(['route_int_id', 'vehicle_int_id'])\
    .orderBy(['route_int_id', 'vehicle_int_id', 'arrival_time'])

timeLead = lead(col("arrival_time"), 1).over(window)
stationLead = lead(col("station_int_id"), 1).over(window)
orderLead = lead(col("order_no"), 1).over(window)

# add columns
lpp = lpp\
    .withColumn("station_2_int_id", stationLead)\
    .withColumn("lead_arrival_time", timeLead)\
    .withColumn("lead_order_no", orderLead)

# create user defined function for calculating the difference between station
# arrival time
timeDiff = udf(
    lambda a, b: 0 if a is None else int((a - b).total_seconds()),
    IntegerType())

# create user defined function for calculating the difference between station
# order
orderDiff = udf(lambda a, b: 0 if a is None else int((a - b)), IntegerType())

# add columns
lpp = lpp\
    .withColumn('time_diff',
                timeDiff(col("lead_arrival_time"), col("arrival_time")))\
    .withColumn('order_diff',
                orderDiff(col("lead_order_no"), col("order_no")))

# filter out big differences in time and order
lpp = lpp.filter(col('time_diff').between(1, 1000) & (col('order_diff') == 1))

# add columns with hour and weekday
hourTokens = udf(lambda time: time.hour, IntegerType())
weekTokens = udf(lambda time: time.weekday(), IntegerType())

lpp = lpp\
    .withColumn('weekday', weekTokens(lpp.arrival_time))\
    .withColumn('hour', hourTokens(lpp.arrival_time))

# calculate number of samples and average travel time between two sequential
# stations for every bus for every hour and day of the week
lpp = lpp\
    .groupBy(['route_int_id', col('station_int_id').alias('station_1_int_id'),
              'station_2_int_id', 'weekday', 'hour']) \
    .agg(count("*").alias("number_of_samples"),
         avg("time_diff").alias("travel_time"))

# for accuracy lets take just the travel time calculated from at lest three
# samples
lpp = lpp.filter('number_of_samples >= 3')

# save to cassandra
lpp.write\
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table="lpp_travel_time", keyspace="dice_results") \
    .save()
