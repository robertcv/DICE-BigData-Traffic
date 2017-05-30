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

default['DICE-BigData-Traffic']['release_url'] =
        'https://github.com/xlab-si/DICE-BigData-Traffic/archive/0.1.1.tar.gz'
default['DICE-BigData-Traffic']['release_checksum'] =
        'f9392dab910b20390eb586b704ea6a8b6f066a5c57060a326443e8a750f96704'
default['DICE-BigData-Traffic']['cache_path'] = '/tmp/bigdata-traffic'
default['DICE-BigData-Traffic']['user'] = 'dicetraffic'
default['DICE-BigData-Traffic']['group'] = 'dicetraffic'

default['DICE-BigData-Traffic']['config_path'] = '/etc/dicetraffic'
default['DICE-BigData-Traffic']['data_path'] = '/var/lib/dicetraffic'
default['DICE-BigData-Traffic']['btsensors']['server'] = 'datacloud-timon.xlab.si:443'

default['DICE-BigData-Traffic']['config'] = {
# Kafka address set in kafka_fqdn Cloudify runtime attribute; port hardcoded
#    :kafka_host => '127.0.0.1:9092',
    :bt_sensors => {
        :timon_username => 'timon_username',
        :timon_password => 'timon_password',
    },
}

default['DICE-BigData-Traffic']['stream_reactor']['url'] =
        'https://github.com/datamountaineer/stream-reactor/releases/download/v0.2.4/stream-reactor-0.2.4-3.1.1.tar.gz'
default['DICE-BigData-Traffic']['stream_reactor']['release_checksum'] =
        '65bf3da83d6b5dd6aa297c7cbcfb3285c69acd00436475d7980f35b5214b94c0'
default['DICE-BigData-Traffic']['stream_reactor']['install_path'] =
        '/var/lib/stream-reactor'

# Cassandra address set in cassandra_fqdn Cloudify runtime attribute
#default['DICE-BigData-Traffic']['stream_reactor']['cassandra_address'] =
#        '127.0.0.1'
default['DICE-BigData-Traffic']['stream_reactor']['cassandra_port'] = 9042
default['DICE-BigData-Traffic']['stream_reactor']['cassandra_keyspace'] =
        'bigdatatraffic'
default['DICE-BigData-Traffic']['stream_reactor']['cassandra_username'] =
        'username'
default['DICE-BigData-Traffic']['stream_reactor']['cassandra_password'] =
        'password'
# Kafka-related parameters
default['DICE-BigData-Traffic']['stream_reactor']['kafka_user'] = 'kafka'
default['DICE-BigData-Traffic']['stream_reactor']['kafka_home'] =
    '/usr/share/kafka'
default['DICE-BigData-Traffic']['stream_reactor']['kafka_log_dir'] =
    '/var/log/kafka'

# Settings for VPN - only the private key for now to be supplied externally
default['DICE-BigData-Traffic']['vpn_key'] = 'dummy'