require 'serverspec'
set :backend, :exec

describe package('openvpn') do
    it { should be_installed }
end

describe file('/etc/openvpn/arctur.conf') do
    it { should exist }
    it { should be_file }
    it { should contain 'cert arctur-vpn/arctur-openstack-vpn-client.crt' }
    it { should contain 'key arctur-vpn/arctur-openstack-vpn-client.key' }
end

describe file('/etc/openvpn/arctur-vpn/arctur-openstack-vpn-client.crt') do
    it { should exist }
    it { should be_file }
    it { should contain 'Subject: C=SI, L=Ljubljana, O=XLAB d.o.o., OU=XLAB research, CN=arctur-openstack-vpn-client/name=arctur-openstack/emailAddress=admin@xlab.si' }
end

describe file('/etc/openvpn/arctur-vpn/arctur-openstack-vpn-client.key') do
    it { should exist }
    it { should be_file }
    it { should contain '-----BEGIN PRIVATE KEY-----' }
    it { should contain 'MIIEvERYLLONGgibbrishLO0kINGtextIMITATinguuenCODEbas64privatekey' }
    it { should contain '43+xNwwfueIOidf3djg2331=' }
    it { should contain '-----END PRIVATE KEY-----' }
    it { should_not contain '--- MIIE' }
end
