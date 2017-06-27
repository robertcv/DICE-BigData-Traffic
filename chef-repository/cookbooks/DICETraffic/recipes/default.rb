#
# Cookbook Name:: DICETraffic
# Recipe:: default
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

release_url = node['DICE-BigData-Traffic']['release_url']
checksum = node['DICE-BigData-Traffic']['checksum']

release_tar = "#{Chef::Config[:file_cache_path]}/dice-bigdata-traffic.tar.gz"
remote_file release_tar do
  source release_url
  checksum checksum
  action :create
end

cache_path = node['DICE-BigData-Traffic']['cache_path']
directory cache_path do
    action :create
end

poise_archive release_tar do
    destination cache_path
end

dicetraffic_user = node['DICE-BigData-Traffic']['user']
dicetraffic_group = node['DICE-BigData-Traffic']['group']

group dicetraffic_group

user node['DICE-BigData-Traffic']['user'] do
    group dicetraffic_group
    shell '/bin/bash'
end

config_path = node['DICE-BigData-Traffic']['config_path']
directory config_path do
    user dicetraffic_user
    group dicetraffic_group
    mode '0755'
    action :create
end

data_path = "#{node['DICE-BigData-Traffic']['data_path']}/data"
[node['DICE-BigData-Traffic']['data_path'], data_path].each do |path|
    directory path do
        user dicetraffic_user
        group dicetraffic_group
        mode '0755'
        recursive true
        action :create
    end
end