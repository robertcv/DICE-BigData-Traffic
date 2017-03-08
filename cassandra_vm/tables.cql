CREATE KEYSPACE dice WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
USE dice;

// bt_senzors

CREATE table bt_sensors (id varchar, fromBtId varchar, fromBtLng float, fromBtLat float, toBtId varchar, toBtLng float,
toBtLat float, distance int, allCount int, avgSpeed float, avgTravelTime float, count int, timestampFrom timestamp,
timestampTo timestamp, PRIMARY KEY (id, timestampTo))
WITH CLUSTERING ORDER BY (timestampTo DESC);
CREATE INDEX ON bt_sensors(fromBtId);
CREATE INDEX ON bt_sensors(toBtId);