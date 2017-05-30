resource_name 'set_hostname'

property :hostname, String, name_property: true
property :fqdn, String
property :marker, String

action :set do
  ohai 'reload hostname' do
    plugin 'hostname'
    action :nothing
  end

  execute "hostname #{hostname}" do
    notifies :reload, 'ohai[reload hostname]'
  end

  if ::File.exist?('/usr/bin/hostnamectl')
    execute "hostnamectl set-hostname #{hostname}" do
      notifies :reload, 'ohai[reload hostname]'
    end
  else
    file '/etc/hostname' do
      content "#{hostname}\n"
      mode '0644'
      notifies :reload, 'ohai[reload hostname]'
    end
  end

  template '/etc/hosts' do
    source 'hosts.erb'
    owner 'root'
    group 'root'
    mode 0644
    variables(
      ip: node['ipaddress'], fqdn: fqdn, hostname: hostname, marker: marker
    )
  end
end

def after_created
  Array(action).each do |action|
    self.run_action(action)
  end
end
