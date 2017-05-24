# Cookbook Name:: DICETraffic
# Recipe:: stream_reactor_config
#
# Copyright 2017, XLAB d.o.o.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

rt_props = node['cloudify']['runtime_properties']
node_stream_reactor = node['DICE-BigData-Traffic']['stream_reactor']
install_path = node_stream_reactor['install_path']
release_url = node_stream_reactor['url']
release_checksum = node_stream_reactor['release_checksum']
kafka_home = node_stream_reactor['kafka_home']

dicetraffic_user = node['DICE-BigData-Traffic']['user']
dicetraffic_group = node['DICE-BigData-Traffic']['group']

# modify Kafka configuration (do we need to do this on all Kafkas?)
ruby_block "disable schemas in kafka" do
    block do
        cfg = Chef::Util::FileEdit.new(
            "#{kafka_home}/config/connect-distributed.properties")
        cfg.search_file_replace(/schemas\.enable=true/, 'schemas_enable=false')
        cfg.write_file if cfg.unwritten_changes?
    end
end

# Service to run the stream reactor
template "/etc/init/stream-reactor.conf" do
    source "stream-reactor.conf.erb"
    mode '0644'
    variables kafka_user: node_stream_reactor['kafka_user'],
            kafka_home: node_stream_reactor['kafka_home'],
            kafka_log_dir: node_stream_reactor['kafka_log_dir'],
            stream_reactor_home: install_path
end

service 'stream-reactor' do
    action [ :enable, :start ]
end

# Configurations for all sources
config_files = [
        {
            :fname => 'cassandra-sink-bt-sensors.properties',
            :name => 'cs-bt-sensors',
            :topic => 'bt_json',
            :table => 'bt_sensors',
        },
        {
            :fname => 'cassandra-sink-inductive-loops.properties',
            :name => 'cs-inductive-loops',
            :topic => 'inductive_json',
            :table => 'inductive_loops',
        },
        {
            :fname => 'cassandra-sink-counters.properties',
            :name => 'cs-counters',
            :topic => 'counter_json',
            :table => 'counters',
        },
        {
            :fname => 'cassandra-sink-pollution.properties',
            :name => 'cs-pollution',
            :topic => 'pollution_json',
            :table => 'pollution',
        },
        {
            :fname => 'cassandra-sink-lpp-station.properties',
            :name => 'cs-lpp-station',
            :topic => 'lpp_station_json',
            :table => 'lpp_station',
        },
        {
            :fname => 'cassandra-sink-lpp-static.properties',
            :name => 'cs-lpp-static',
            :topic => 'lpp_static_json',
            :table => 'lpp_static',
        },
        {
            :fname => 'cassandra-sink-lpp-live.properties',
            :name => 'cs-lpp-live',
            :topic => 'lpp_live_json',
            :table => 'lpp_live',
        }
    ]

config_path = "#{install_path}/conf"
config_files.each do | config |
    config_fname = "#{config_path}/#{config[:fname]}"
    config[:cassandra_address] = rt_props['cassandra_fqdn']
    config[:cassandra_port] = node_stream_reactor[:cassandra_port]
    config[:keyspace] = node_stream_reactor[:cassandra_keyspace]
    config[:cassandra_username] = node_stream_reactor[:cassandra_username]
    config[:cassandra_password] = node_stream_reactor[:cassandra_password]

    template config_fname do
        source 'cassandra-sink.properties.erb'
        variables config
    end

    bash "start source #{config[:name]}" do
        code <<-EOH
            set -e
            bin/cli.sh create #{config[:name]} < #{config_fname}
            EOH
        cwd install_path
        retries 15
    end

    service 'stream-reactor' do
        action :restart
    end
end
