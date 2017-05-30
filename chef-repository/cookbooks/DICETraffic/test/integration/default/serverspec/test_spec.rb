require 'serverspec'
set :backend, :exec

describe group('dicetraffic') do
    it { should exist }
end

describe user('dicetraffic') do
    it { should exist }
    it { should belong_to_primary_group 'dicetraffic' }
end

describe file('/tmp/bigdata-traffic') do
    it { should exist }
    it { should be_directory }
end

describe file('/tmp/bigdata-traffic/python_package/pytraffic/') do
    it { should exist }
    it { should be_directory }
end

describe file('/tmp/bigdata-traffic/python_package/requirements.txt') do
    it { should be_file }
end

dirs = %w(/etc/dicetraffic /var/lib/dicetraffic)
dirs.each do |dir|
    describe file(dir) do
        it { should exist }
        it { should be_directory }
        it { should be_owned_by 'dicetraffic' }
        it { should be_grouped_into 'dicetraffic' }
        it { should be_mode 755 }
    end
end