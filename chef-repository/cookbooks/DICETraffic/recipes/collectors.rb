#
# Cookbook Name:: DICETraffic
# Recipe:: collectors
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

config_path = node['DICE-BigData-Traffic']['config_path']
data_path = node['DICE-BigData-Traffic']['data_path']
rt_props = node['cloudify']['runtime_properties']

python_runtime '3'

# install the command line tool and the appropriate modules and requirements
cache_path = node['DICE-BigData-Traffic']['cache_path']
python_execute 'setup pytraffic' do
    command "-m pip install ."
    cwd "#{cache_path}/python_package/"
    user 'root'
    group 'root'
end

# obtain and store the client certificate
btsensors_server = node['DICE-BigData-Traffic']['btsensors']['server']
certificate_file = "datacloud.crt"
execute 'obtain timon cert' do
    command "openssl s_client -showcerts -connect #{btsensors_server} < /dev/null > #{certificate_file}"
    cwd config_path
end

# create the configuration file
config = node['DICE-BigData-Traffic']['config'].to_hash.dup
config['kafka_host'] = "#{rt_props['kafka_fqdn']}:9092"
config['bt_sensors'] = config['bt_sensors'].to_hash.dup
config['bt_sensors']['timon_crt_file'] = "#{config_path}/#{certificate_file}"
config['data_dir'] = File.join(data_path, '') # trailing delim. important because software.

template "#{config_path}/local.conf" do
    source 'local.conf.erb'
    variables json: config
end

# configure and enable systemd units - services and timers
systemd_units = {
    'lpp_daily' => {
        :description => 'Send lpp station and static arrival data to Kafka.',
        :parameters => '--lpp_collector station',
        :calendar => '*-*-* 00:00:00',
    },
    'lpp_minutely' => {
        :description => 'Send lpp live arrival to Kafka.',
        :parameters => '--lpp_collector live',
        :calendar => '*-*-* *:*:00',
    },
    'pollution_hourly' => {
        :description => 'Send pollution data to Kafka.',
        :parameters => '--pollution_collector',
        :calendar => '*-*-* *:00:00',
    },
    'bluetooth_quarter-hourly' => {
        :description => 'Send bluetooth sensors data to Kafka.',
        :parameters => '--bt_collector',
        :calendar => '*-*-* *:0/15:00',
    },
    'loops_counters_quarter-hourly' => {
        :description => 'Send inductive loops and counters data to Kafka.',
        :parameters => '--il_collector --counters_collector',
        :calendar => '*-*-* *:0/15:00',
    },
}

systemd_units.each do | unit, data |
    data[:config_path] = config_path
    data[:unit] = "#{unit}.service"

    template "/etc/systemd/system/#{unit}.service" do
      source 'generic.service.erb'
      variables data
    end

    template "/etc/systemd/system/#{unit}.timer" do
      source 'generic.timer.erb'
      variables data
    end

    execute 'systemctl daemon-reload'

    service "#{unit}.service" do
        action :enable
    end

    service "#{unit}.timer" do
        action [ :enable, :start ]
    end
end