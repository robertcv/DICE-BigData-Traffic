## Spark

Run Apache Spark locally:

```bash
export SPARK_HOME=/home/ubuntu/spark-2.0.1-bin-hadoop2.7
./run_spark_local.sh cassandra_ip app.py arg1 arg2
```

Run it on cluster (on master):

```bash
./run_spark_cluster.sh cassandra_ip spark://hostname:7077 app.py arg1 arg2
```

### Apps

#### HeavyTraffic

This Spark app fetches data of inductive loops and counters from Cassandra, then
selects the rows with heavy traffic and saves them back to a new table in
Cassandra.

Data:
* source: Cassandra, key space dice, table inductive_loops and counters
* sink: Cassandra, key space dice_results, table heavy_traffic

#### TrafficForecast

This Spark app takes counters and inductive loops data from Cassandra,
transforms and uses it to train a classifier to predict traffic data for the
next day.

Args:
* \#1: Datetime in iso format from which the program should forecast traffic
data.
* \#2: Datetime in iso format to which the program should forecast traffic data.

Data:
* source: Cassandra, key space dice, table inductive_loops and counters
* sink: Cassandra, key space dice_results, table traffic_forecast

#### TrafficAnimation

This Spark app takes counters and inductive loops data from Cassandra and create
an animation of traffic on given day.

Args:
* \#1: Day of week starting with monday as 0.
* \#2: Start time from which the program animates traffic data.
* \#3: End time to which the program animates traffic data.

Data:
* source: Cassandra, key space dice, table inductive_loops and counters
* sink: Spark master, traffic_weekday_X.gif file

#### LppStationOrder

This Spark app takes lpp buses arrival times from Cassandra and generates a list
of sequential stations for every bus route. The data is then saved back to
Cassandra.

Data:
* source: Cassandra, key space dice, table inductive_loops and counters
* sink: Cassandra, key space dice_results, table lpp_station_order

#### LppTravelTime

This Spark app takes lpp buses arrival times from Cassandra and calculates
average travel time between two bus stations for every bus on every hour and
day of the week. This data is then saved back to Cassandra. Because the app
needs station order data the app LppStationOrder has to be run beforehand. 

Data:
* source: Cassandra, key space dice, table inductive_loops and counters; key
space dice_results, lpp_station_order
* sink: Cassandra, key space dice_results, table lpp_travel_time