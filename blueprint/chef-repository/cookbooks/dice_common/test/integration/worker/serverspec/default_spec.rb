require 'serverspec'
set :backend, :exec

describe file('/etc/hosts') do
  it { should be_file }
  it { should be_mode 644 }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
  its(:content) do
    should contain "#{host_inventory['hostname']}.node.consul"
  end
end

describe group('consul') do
  it { should exist }
end

describe user('consul') do
  it { should exist }
  it { should belong_to_primary_group 'consul' }
end

describe file('/var/lib/consul') do
  it { should be_directory }
  it { should be_mode 755 }
  it { should be_owned_by 'consul' }
end

describe service('consul-agent') do
  it { should be_enabled }
  it { should be_running }
end

describe port(8301) do
  it { should be_listening.with('tcp') }
  it { should be_listening.with('udp') }
end

describe file('/etc/resolv.conf') do
  it { should be_file }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
  its(:content) do
    should include 'nameserver 8.8.8.8'
  end
end

describe host_inventory['hostname'] do
  it { should match(/^a1b2c3-(abcdefghi-){4}-[0-9a-fA-F]{12}$/) }
end
