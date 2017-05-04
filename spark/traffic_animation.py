from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, avg
from pyspark.sql.types import DoubleType, DateType

import sys
import time
import datetime
from collections import defaultdict

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.img_tiles import OSM
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

"""
This Spark app takes counters and inductive loops data from Cassandra and create
an animation of traffic on given day.

Args:
    #1: Day of week starting with monday as 0.
    #2: Time in from which the program animates traffic data.
    #3: Time in to which the program animates traffic data.

Example:

    $ spark-submit \
    --packages com.datastax.spark:spark-cassandra-connector_2.11:2.0.0-M3 \
    --conf spark.cassandra.connection.host=127.0.0.2 \
    --master spark://127.0.0.1:7077 \
    traffic_forecast.py 0 07:00 12:00

"""

spark = SparkSession.builder \
    .appName("TrafficAnimation") \
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
    col('stevci_smeropis').alias('direction'),
    col('x_wgs').alias('longitude'),
    col('y_wgs').alias('latitude'),
    col('modified').alias('datetime2'))

tmp_il = il.where('stat!=0').select(
    'id',
    'stat',
    col('directionDescription').alias('direction'),
    col('deviceY').alias('longitude'),
    col('deviceX').alias('latitude'),
    col('updated').alias('datetime2'))

traffic = tmp_counters.union(tmp_il)

# transform data
delta = time.altzone if time.daylight else time.timezone

timeTokens = udf(
    lambda time: time - datetime.timedelta(seconds=delta), DateType())
traffic = traffic.withColumn('datetime', timeTokens(traffic.datetime2))

quarterTokens = udf(
    lambda time: float(time.hour * 4 + time.minute / 15), DoubleType())
traffic = traffic.withColumn('quarter', quarterTokens(traffic.datetime))

weekdayTokens = udf(lambda time: float(time.weekday()), DoubleType())
traffic = traffic.withColumn('weekday', weekdayTokens(traffic.datetime))

# This is because no traffic is set to 6, but a more reasonable number is 0.
# Now traffic density increases from no traffic - 0, normal traffic - 1, ...,
# traffic congestion - 5.
statTokens = udf(lambda stat: 0.0 if stat == 6 else float(stat), DoubleType())
traffic = traffic.withColumn('stat', statTokens('stat'))

# get average traffic status for given day
weekday = sys.argv[1]
start = datetime.datetime.strptime(sys.argv[2], "%H:%M")
start_quarter = start.hour * 4 + start.minute / 15
end = datetime.datetime.strptime(sys.argv[3], "%H:%M")
end_quarter = end.hour * 4 + end.minute / 15

day_traffic = traffic \
    .filter(traffic.weekday == weekday) \
    .groupBy('direction', 'longitude', 'latitude', 'quarter') \
    .agg(avg('stat').alias('stat'))
day_traffic = day_traffic.collect()

# prepare data for plotting
lng = defaultdict(list)
lat = defaultdict(list)
stat = defaultdict(list)
for row in day_traffic:
    quarter = int(row['quarter'])
    if start_quarter <= quarter <= end_quarter:
        lng[quarter].append(row['longitude'])
        lat[quarter].append(row['latitude'])
        stat[quarter].append(row['stat'])

# create animation
vmax = 5.0
cmap = LinearSegmentedColormap.from_list('mycmap', [(0 / vmax, 'green'),
                                                    (2 / vmax, 'yellow'),
                                                    (4 / vmax, 'red'),
                                                    (5 / vmax, 'red')])
norm = plt.Normalize(0, 5)
imagery = OSM()
fig = plt.figure(figsize=(10, 10), dpi=120)
ax = plt.axes(projection=imagery.crs)
ax.set_extent((14.42, 14.6, 46.0, 46.09))
ax.add_image(imagery, 14)
ax.text(0.43, 1.03, 'Promet v Ljubljani', transform=ax.transAxes)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
scat = plt.scatter(lng[start_quarter], lat[start_quarter],
                   c=stat[start_quarter], transform=ccrs.Geodetic(), cmap=cmap,
                   norm=norm)


def animate(i):
    h = i / 4
    m = 15 * (i % 4)
    label = 'Ob: {:02}:{:02}'.format(h, m)
    data = np.hstack((
        np.asarray(lng[i])[:, np.newaxis],
        np.asarray(lat[i])[:, np.newaxis]))
    scat.set_offsets(data)
    scat.set_array(np.asarray(stat[i]))
    time_text.set_text(label)
    return scat, time_text


ani = FuncAnimation(fig, animate, np.arange(start_quarter, end_quarter),
                    interval=1000, blit=True)

ani.save('traffic_weekday_' + str(weekday) + '.gif')
