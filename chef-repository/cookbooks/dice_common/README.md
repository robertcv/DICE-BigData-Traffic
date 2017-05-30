# Cookbook for doing initial host setup

This cookbook contains various recipes for preparing hosts.


## Host recipe

This recipe sets entries in `/etc/hosts` file to something reasonable for vast
majority of scenarios where DNS services are not provided natively (for
example, when deploying to OpenStack).

After this recipe has been executed, underlying node can be accessed by using
FQDN in the form of `$(hostname).node.consul`, where hostname is machine's
hostname.

Note that in order for this lookup to work properly, custom DNS server needs
to be installed that redirects `*.consul` queries to consul server. DICE
deployment service cookbook supports this kind of DNS server.


## DNS redirecting

In order to make it easier to redirect DNS queries to custom DNS server,
`dns_redirect` recipe is provided. This recipe relies on Cloudify to provide
`dns_server` attribute that holds ip address of custom DNS server.

In most cases, this attribute will be properly set by DICE deployment service
when deploying blueprint. For manual setup, see `.kitchen.yml` file in the
root folder of repository or read comments in default attributes file.


## Dynamic DNS

In order for dynamic DNS system to work properly, each host needs to have
consul client installed that reports to consul server (most commonly installed
along side custom DNS server). Two recipes are provided to help with this
task:

  * consul_common recipe will install common files while
  * consul_agent will install and start consul agent service.


# Common usage

Using this cookbook when setting up worker nodes is really simple: just make
sure `apt::default` recipe is called before any of the recipes in this
cookbook. After that, simply use `default` recipe that will configure worker
node.

For sample run list, consult `.kitchen.yml` file.
