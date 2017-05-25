require 'serverspec'
set :backend, :exec

describe file('/var/lib/stream-reactor') do
    it { should exist }
    it { should be_directory }
    it { should be_owned_by 'dicetraffic' }
    it { should be_grouped_into 'dicetraffic' }
    it { should be_mode 755 }
end

describe file('/var/lib/stream-reactor/bin/cli.sh') do
    it { should exist }
    it { should be_file }
    it { should be_executable }
end

config_path = '/var/lib/stream-reactor/conf'
config_files = [
        {"cassandra-sink-bt-sensors.properties": [
            "name=cs-bt-sensors",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO bt_sensors SELECT * FROM bt_json",
            "cs-bt-sensors"]},
        {"cassandra-sink-counters.properties": [
            "name=cs-counters",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO counters SELECT * FROM counter_json",
            "cs-counters"]},
        {"cassandra-sink-inductive-loops.properties": [
            "name=cs-inductive-loops",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO inductive_loops SELECT * FROM inductive_json",
            "cs-inductive-loops"]},
        {"cassandra-sink-lpp-live.properties": [
            "name=cs-lpp-live",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO lpp_live SELECT * FROM lpp_live_json",
            "cs-lpp-live"]},
        {"cassandra-sink-lpp-static.properties": [
            "name=cs-lpp-static",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO lpp_static SELECT * FROM lpp_static_json",
            "cs-lpp-static"]},
        {"cassandra-sink-lpp-station.properties": [
            "name=cs-lpp-station",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO lpp_station SELECT * FROM lpp_station_json",
            "cs-lpp-station"]},
        {"cassandra-sink-pollution.properties": [
            "name=cs-pollution",
            "connector.class=com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector",
            "connect.cassandra.sink.kcql=INSERT INTO pollution SELECT * FROM pollution_json",
            "cs-pollution"]},
    ]

config_files.each do | config_data |
    fname = config_data.keys[0]
    entries = config_data[fname]
    describe file("#{config_path}/#{fname}") do
        it { should exist }
        it { should be_file }
        it { should be_owned_by 'root' }
        it { should be_grouped_into 'root' }
        it { should be_mode 644 }
        it { should contain "connect.cassandra.contact.points=cassandra22.local.lan" }
        it { should contain "connect.cassandra.port=9042" }
        it { should contain "connect.cassandra.key.space=kitchenspace" }
        it { should contain entries[0] }
        it { should contain entries[1] }
        it { should contain entries[2] }
    end

    describe file('/tmp/stream-reactor-mock-cli.log') do
        it { should contain "create #{entries[3]}" }
    end
end
