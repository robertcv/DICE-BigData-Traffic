# Cookbook Name:: DICETraffic
# Recipe:: vpn_install
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

package 'openvpn' do
    action :install
end

directory '/etc/openvpn/arctur-vpn' do
    action :create
end

files = [
        ['/etc/openvpn/arctur.conf', 'arctur.ovpn'],
        ['/etc/openvpn/arctur-vpn/arctur-openstack-vpn-client.crt', 'arctur-openstack-vpn-client.crt'],
        ['/etc/openvpn/arctur-vpn/ca.crt', 'ca.crt'],
    ]

files.each do | f |
    cookbook_file f[0] do
        source f[1]
        action :create
    end
end

file '/etc/openvpn/arctur-vpn/arctur-openstack-vpn-client.key' do
    content node['DICE-BigData-Traffic']['vpn_key']
    action :create
end