## Collectors

Here are all collectors for scraping data from different sources and
forwarding it the data in json format to Apache Kafka. The main scripts 
have kafka in their names. There are also some other files for which 
purposes reference the readme.

For running the scripts you need some additional python modules which 
you can install using pip:

```
pip install --upgrade pip
pip install -r requirements.txt
```

and for ploting scripts:

```
pip install -r requirements-plot.txt
```

Every collector forwards his data to his unique Kafka topic. A Kafka 
connector then takes those json messages and inserts them into Cassandra
[tables](../virtual_machines/cassandra_vm/tables.cql).

|      Collector     |    Kafka topic   | Cassandra table |
|:------------------:|:----------------:|:---------------:|
|  Bluetooth sensors |      bt_json     |    bt_sensors   |
|  Traffic counters  |   counter_json   |     counters    |
|   Inductive loops  |  inductive_json  | inductive_loops |
|  LPP stations data | lpp_station_json |   lpp_station   |
| LPP static arrival |  lpp_static_json |    lpp_static   |
|  LPP live arrival  |   lpp_live_json  |     lpp_live    |
|    Air pollution   |  pollution_json  |    pollution    |
