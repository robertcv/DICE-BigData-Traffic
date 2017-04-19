from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

conf = SparkConf()
conf.setAppName("HeavyTraffic")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

counters = sqlContext \
    .read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="counters", keyspace="dice")

il = sqlContext \
    .read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="inductive_loops", keyspace="dice")

statTokens = udf(
    lambda
        stat: 'Heavy traffic' if stat == 'Gost promet' else 'Traffic congestion',
    StringType())
counters = counters.withColumn('stat', statTokens(counters.stevci_statopis))
laneTokens = udf(lambda lane: '(d)' if lane == '(v)' else '(o)', StringType())
counters = counters.withColumn('lane', laneTokens(counters.stevci_pasopis))

il = il.fillna({'lanedescription': ' '})

counters = counters \
    .where('stevci_stat==4 or stevci_stat=5') \
    .select('id',
            col('stevci_lokacijaopis').alias('location'),
            col('stevci_cestaopis').alias('road'),
            col('stevci_smeropis').alias('direction'),
            'lane',
            'stat',
            col('x_wgs').alias('longitude'),
            col('y_wgs').alias('latitude'),
            col('modified').alias('datetime'))

il = il \
    .where('stat==4 or stat=5') \
    .select('id',
            col('locationDescription').alias('location'),
            col('roadDescription').alias('road'),
            col('directionDescription').alias('direction'),
            col('laneDescription').alias('lane'),
            col('StatusDescription').alias('stat'),
            col('deviceY').alias('longitude'),
            col('deviceX').alias('latitude'),
            col('updated').alias('datetime'))

heavy_traffic = counters.unionAll(il)

heavy_traffic.write \
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table="heavy_traffic", keyspace="dice_results") \
    .save()
