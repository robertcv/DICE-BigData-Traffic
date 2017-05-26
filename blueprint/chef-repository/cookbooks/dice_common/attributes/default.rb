# Cookbook Name:: dice_common
# Attribute:: default
#
# Copyright 2016, XLAB d.o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

default['dice_common']['consul-zip'] =
  'https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_amd64.zip'
default['dice_common']['consul-sha256sum'] =
  'abdf0e1856292468e2c9971420d73b805e93888e006c76324ae39416edcf0627'

# Cloudify provided attributes (do not uncomment this, this is here for
# documentation purpose only):
#
# Address of custom DNS server (most of the time, this attribute will be
# injected by DICE deployment service.
# default['cloudify']['properties']['dns_server'] = 8.8.8.8
