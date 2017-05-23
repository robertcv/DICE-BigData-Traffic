require 'serverspec'
set :backend, :exec

# verify the existence of the CLI tool
describe file('/usr/local/bin/pytraffic') do
    it { should exist }
    it { should be_file }
    it { should be_executable }
end

describe command('pytraffic --help') do
    its(:exit_status) { should eq 0 }
end

# check the configuration
describe file('/etc/dicetraffic/local.conf') do
    it { should exist }
    it { should be_file }
    it { should contain '"kafka_host": "mykafka.local.lan:9092"' }
    it { should contain '"timon_username": "blueadmin"' }
    it { should contain '"timon_password": "toothsword"' }
    it { should contain '"timon_password": "toothsword"' }
    it { should contain '"timon_crt_file": "/etc/dicetraffic/datacloud.crt"' }
end

# verify the systemd services and timers
systemd_units = [
        ['lpp_daily', '--lpp_collector station', '*-*-* 00:00:00'],
        ['lpp_minutely', '--lpp_collector live', '*-*-* *:*:00'],
        ['pollution_hourly', '--pollution_collector', '*-*-* *:00:00'],
        ['pytraffic', '--bt_collector --il_collector --counters_collector',
            '*-*-* *:0/15:00'],
    ]

systemd_units.each do | unit_array |
    describe file("/etc/systemd/system/#{unit_array[0]}.service") do
        it { should exist }
        it { should be_file }
        it { should contain unit_array[1] }
    end

    describe file("/etc/systemd/system/#{unit_array[0]}.timer") do
        it { should exist }
        it { should be_file }
        it { should contain unit_array[2] }
        it { should contain "Unit=#{unit_array[0]}.service" }
    end

    describe service(unit_array[0]) do
        it { should be_enabled }
    end
end

# check the Timon's data server's certificate
describe file('/etc/dicetraffic/datacloud.crt') do
    it { should exist }
    it { should be_file }
    it { should contain '-----BEGIN CERTIFICATE-----'}
end
