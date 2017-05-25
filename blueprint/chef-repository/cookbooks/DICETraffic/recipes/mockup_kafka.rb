# Cookbook Name:: DICETraffic
# Recipe:: mockup_kafka
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

# This recipe is for testing purposes only and should be used only in .kitchen
# environment or similar. It is here to (re)create the files and commands
# to make kitchen feel like there is a Kafka installation on the node and
# that there are commands that can be called to register configurations to
# various external services.

node_stream_reactor = node['DICE-BigData-Traffic']['stream_reactor']
install_path = node_stream_reactor['install_path']
kafka_home = node_stream_reactor['kafka_home']

mock_log_file = '/tmp/stream-reactor-mock-cli.log'
file mock_log_file do
    action :delete
end

template "#{install_path}/bin/cli.sh" do
    source 'mockup-call.sh.erb'
    variables logfile: mock_log_file
    mode '0755'
    action :create
end

kafka_user = node_stream_reactor['kafka_user']
group kafka_user

user kafka_user do
    group kafka_user
    shell '/bin/bash'
end

[ '', '/bin', '/config' ].each do |dir|
    directory "#{kafka_home}#{dir}" do
        recursive true
        action :create
    end
end

file "#{kafka_home}/bin/connect-distributed.sh" do
    content <<-EOH
        #!/bin/bash

        sleep 1000
        EOH
    mode '0755'
end

file "#{kafka_home}/config/connect-distributed.properties" do
    content <<-EOH
        # mock-up content for testing purposes
        bootstrap.servers=localhost:9092
        group.id=connect-cluster
        key.converter=org.apache.kafka.connect.json.JsonConverter
        value.converter=org.apache.kafka.connect.json.JsonConverter
        key.converter.schemas.enable=true
        value.converter.schemas.enable=true
        offset.storage.topic=connect-offsets
        # etc.
        EOH
    mode '0644'
end
