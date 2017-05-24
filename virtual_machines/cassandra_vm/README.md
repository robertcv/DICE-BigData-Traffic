## Apache Cassandra

The Kafka connector and Spark which send data to Cassandra expect precreated
tables and keyspace. So after installing and starting Cassandra we run
`tables.cql` which creates keyspaces and tables.

### Keyspace dice

#### Table bt_sensors
| columns | type |
|:---------:|:---------:|
| id | varchar |
| fromBtId | varchar |
| fromBtLng | float |
| fromBtLat | float| 
| toBtId | varchar | 
| toBtLng | float |
| toBtLat | float |
| distance | int |
| allCount | int |
| avgSpeed | float |
| avgTravelTime | float |
| count | int |
| timestampFrom | timestamp |
| timestampTo | timestamp |

#### Table inductive_loops

| columns | type |
|:---------:|:---------:|
| id | varchar |
| title | varchar |
| region | varchar |
| location | int |
| locationDescription | varchar |
| deviceX | float |
| deviceY | float |
| point | varchar |
| direction | int |
| directionDescription| varchar |
| laneDescription | varchar |
| roadSection | varchar |
| roadDescription | varchar |
| StatusDescription | varchar |
| numberOfVehicles | int |
| gap | float |
| vmax | int |
| avgSpeed | int |
| occ | int |
| chainage | int |
| stat | int |
| time | varchar |
| date | varchar |
| pkgdate | timestamp |
| updated | timestamp |

#### Table counters

| columns | type |
|:---------:|:---------:|
| id | varchar |
| Title | varchar |
| Description | varchar |
| stevci_lokacijaOpis | varchar |
| stevci_cestaOpis | varchar |
| stevci_smerOpis| varchar |
| stevci_pasOpis | varchar |
| x_wgs | float |
| y_wgs | float |
| CrsId | varchar |
| Y | float |
| X | float |
| stevci_statOpis | varchar |
| stevci_stev | int |
| stevci_hit | int |
| stevci_gap | float |
| stevci_stat | int |
| ContentName | varchar |
| Icon | varchar |
| modified | timestamp |

#### Table pollution

| columns | type |
|:---------:|:---------:|
| location | varchar |
| co | float |
| no | float |
| no2 | float |
| nox | float |
| pm | float |
| so2 | float |
| solar_radiation | float |
| temperature | float |
| pressure | float |
| humidity | float |
| windspeed | float |
| wind_direction | varchar |
| paraxylene | float |
| benzene | float |
| tolulene | float |
| hour | varchar |
| scraped | timestamp |

#### Table lpp_station

| columns | type |
|:---------:|:---------:|
| station_int_id | int |
| station_name | varchar |
| station_direction | varchar |
| station_ref_id | int |
| station_lat | float |
| station_lng | float |
| route_int_id | int |
| route_length | float |
| route_num | int |
| route_num_sub | varchar |
| route_name | varchar |
| scraped | timestamp |

#### Table lpp_static

| columns | type |
|:---------:|:---------:|
| station_int_id | int |
| route_int_id | int |
| arrival_time | timestamp |

#### Table lpp_live

| columns | type |
|:---------:|:---------:|
| station_int_id | int |
| route_int_id | int |
| vehicle_int_id | int |
| arrival_time | timestamp |

### Keyspace dice_results

#### Table heavy_traffic

| columns | type |
|:---------:|:---------:|
| id | varchar |
| location | varchar |
| road | varchar |
| direction | varchar |
| lane | varchar |
| stat | varchar |
| longitude | float |
| latitude | float |
| datetime | timestamp |

#### Table traffic_forecast

| columns | type |
|:---------:|:---------:|
| id | varchar |
| stat | varchar |
| datetime | timestamp |

#### Table lpp_station_order

| columns | type |
|:---------:|:---------:|
| route_int_id | int |
| station_int_id | int |
| order_no | int |
| arrival_time | timestamp |

#### Table lpp_travel_time

| columns | type |
|:---------:|:---------:|
| route_int_id | int |
| station_1_int_id | int |
| station_2_int_id | int |
| weekday | int |
| hour | int |
| number_of_samples | int |
| travel_time | float |