from pyspark.sql import SparkSession

import datetime

"""
This Spark app takes lpp buses arrival times from Cassandra and generates a list
of sequential stations for every bus route. The data is then saved back to
Cassandra.
"""

spark = SparkSession.builder \
    .appName("LppStationOrder") \
    .getOrCreate()

lpp_live = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(table="lpp_live", keyspace="dice")

routes = lpp_live.select('route_int_id').distinct().collect()

data = []
for route in routes:
    # sort data by time and vehicle
    route_data = lpp_live \
        .filter('route_int_id=' + str(route.route_int_id)) \
        .orderBy(["vehicle_int_id", "arrival_time"]) \
        .toPandas()
    # do not use duplicate entry
    route_data = route_data[route_data.diff().station_int_id != 0]
    route_data = route_data.reset_index(drop=True)

    # get indexes of starts of new bus rounds
    diff = route_data.diff()
    mask = (diff.vehicle_int_id != 0) | \
           (diff.arrival_time > datetime.timedelta(minutes=30))
    index = route_data[mask].index.tolist()

    rounds = []
    # divided data by bus rounds
    for i in range(0, len(index) - 1, 2):
        tmp = route_data.loc[index[i]:index[i + 1] - 1]
        tmp = tmp.drop_duplicates(subset='station_int_id', keep=False)
        rounds.append(tmp)

    # sort data by stations on rounds
    rounds = sorted(rounds, key=lambda x: -len(x))

    # not all stations on a route are in one entry, the next step tries to
    # combine all available data to generate a list of sequential stations
    stations = []
    for r in rounds:
        l = len(r)
        for i in range(l):
            # if the current station is not yet in the finished list
            if r.iloc[i].station_int_id in stations:
                continue
            # those it fit on the end of the list
            elif len(stations) == 0 or \
                    (stations[-1] in set(r.iloc[:i].station_int_id)):
                stations.append(r.iloc[i].station_int_id)
            # or on the beginning
            elif stations[0] in set(r.iloc[i:].station_int_id):
                stations.insert(0, r.iloc[i].station_int_id)
            # or somewhere in between
            elif 0 < i < (l - 1) and \
                            r.iloc[i - 1].station_int_id in stations and \
                            r.iloc[i + 1].station_int_id in stations:

                li = stations.index(r.iloc[i - 1].station_int_id)
                di = stations.index(r.iloc[i + 1].station_int_id)
                if (di - li) == 1:
                    stations.insert(di, r.iloc[i].station_int_id)

    # do not save data from routes with less then 5 found stations
    if len(stations) >= 5:
        for i, s in enumerate(stations):
            data.append((route.route_int_id, int(s), i))

# convert data to spark dataframe and save it back to Cassandra
df = spark \
    .createDataFrame(data,
                     ["route_int_id",
                      "station_int_id",
                      "order_no"]
                     )
df.write \
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table="lpp_station_order", keyspace="dice_results") \
    .save()
