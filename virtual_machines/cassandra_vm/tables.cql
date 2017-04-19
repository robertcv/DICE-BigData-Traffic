CREATE KEYSPACE dice WITH REPLICATION = {'class' : 'SimpleStrategy',
'replication_factor' : 1};
USE dice;

// bt_senzors

CREATE table bt_sensors (id varchar, fromBtId varchar, fromBtLng float,
fromBtLat float, toBtId varchar, toBtLng float, toBtLat float, distance int,
allCount int, avgSpeed float, avgTravelTime float, count int, timestampFrom
timestamp, timestampTo timestamp, PRIMARY KEY (id, timestampTo))
WITH CLUSTERING ORDER BY (timestampTo DESC);
CREATE INDEX ON bt_sensors(fromBtId);
CREATE INDEX ON bt_sensors(toBtId);

// inductive loops

CREATE table inductive_loops (id varchar, title varchar, region varchar,
location int, locationDescription varchar, deviceX float, deviceY float, point
varchar, direction int, directionDescription varchar, laneDescription varchar,
roadSection varchar, roadDescription varchar, StatusDescription varchar,
numberOfVehicles int, gap float, vmax int, avgSpeed int, occ int, chainage int,
stat int, time varchar, date varchar, pkgdate timestamp, updated timestamp,
PRIMARY KEY (id, updated))
WITH CLUSTERING ORDER BY (updated DESC);

// counters

CREATE table counters (id varchar, Title varchar, Description varchar,
stevci_lokacijaOpis varchar, stevci_cestaOpis varchar, stevci_smerOpis varchar,
stevci_pasOpis varchar, x_wgs float, y_wgs float, CrsId varchar, Y float, X
float, stevci_statOpis varchar, stevci_stev int, stevci_hit int, stevci_gap
float, stevci_stat int, ContentName varchar, Icon varchar, modified timestamp,
PRIMARY KEY (id, modified))
WITH CLUSTERING ORDER BY (modified DESC);

// pollution

CREATE table pollution (location varchar, co float, no float, no2 float, nox
float, pm float, so2 float, solar_radiation float, temperature float, pressure
float, humidity float, windspeed float, wind_direction varchar, paraxylene
float, benzene float, tolulene float, hour varchar, scraped timestamp,
PRIMARY KEY (location, scraped))
WITH CLUSTERING ORDER BY (scraped DESC);

// lpp_station

CREATE table lpp_station (station_int_id int, station_name varchar,
station_direction varchar, station_ref_id int, station_lat float, station_lng
float, route_int_id int, route_length float, route_num int, route_num_sub
varchar, route_name varchar, scraped timestamp,
PRIMARY KEY (station_int_id, route_int_id, scraped))
WITH CLUSTERING ORDER BY (route_int_id ASC, scraped DESC);

// lpp_static

CREATE table lpp_static (station_int_id int, route_int_id int, arrival_time
timestamp, PRIMARY KEY (station_int_id, route_int_id, arrival_time))
WITH CLUSTERING ORDER BY (route_int_id ASC, arrival_time DESC);

// lpp_live

CREATE table lpp_live (station_int_id int, route_int_id int, vehicle_int_id int,
arrival_time timestamp,
PRIMARY KEY (station_int_id, route_int_id, arrival_time))
WITH CLUSTERING ORDER BY (route_int_id ASC, arrival_time DESC);


// spark results

CREATE KEYSPACE dice_results WITH REPLICATION = {'class' : 'SimpleStrategy',
'replication_factor' : 1};
USE dice_results;

// heavy traffic location

CREATE table heavy_traffic (id varchar, location varchar, road varchar,
direction varchar, lane varchar, stat varchar, longitude float, latitude float,
datetime timestamp, PRIMARY KEY (id, datetime));