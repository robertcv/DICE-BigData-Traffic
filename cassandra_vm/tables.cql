CREATE KEYSPACE dice WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
USE dice;

// bt_senzors

CREATE table bt_sensors (id varchar, fromBtId varchar, fromBtLng float, fromBtLat float, toBtId varchar, toBtLng float,
toBtLat float, distance int, allCount int, avgSpeed float, avgTravelTime float, count int, timestampFrom timestamp,
timestampTo timestamp, PRIMARY KEY (id, timestampTo))
WITH CLUSTERING ORDER BY (timestampTo DESC);
CREATE INDEX ON bt_sensors(fromBtId);
CREATE INDEX ON bt_sensors(toBtId);

// inductive_json

CREATE table inductive_loops (id varchar, title varchar, region varchar, location int, locationDescription varchar,
deviceX float, deviceY float, point varchar, direction int, directionDescription varchar, laneDescription varchar,
roadSection varchar, roadDescription varchar, StatusDescription varchar, numberOfVehicles int, gap float, vmax int,
avgSpeed int, occ int, chainage int, stat int, time varchar, date varchar, pkgdate timestamp, updated timestamp,
PRIMARY KEY (id, updated))
WITH CLUSTERING ORDER BY (updated DESC);

