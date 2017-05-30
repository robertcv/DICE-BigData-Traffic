# BigData-Transport

This project is a real world example of how to use DICE tools. Its main
purpose is to collect, store and process transportation data in
Ljubljana.

The project contains:

* **python_package** – Set of python scripts (collectors) combined into a python
module for ease of installation via pip and ease of usage via the CLI tool. 
Collectors collect data from different sources and foreword them to Apache
Kafka.

* **virtual_machines** – Set of Vagrantfiles and bash scripts for
deploying VMs for testing purposes. Later those will be replaced with
blueprints.

## Deploying BigData-Transport

To deploy the whole BigData-Transport application, consult the
`blueprint.yaml` located in the `blueprint` subfolder. The application
requires a VPN connection to the TIMON servers located in Arctur test
bed. The user must supply the VPN's private key as the `vpn_key` input
with the blueprint.

We recommend the use of the [DICE Deployment Service][dds] for the
deployment. Assuming that your [command line tool][dds-cli] is properly
configured, the following steps will help deploy the BigData-Transport.

First, obtain the code of the application.

    $ git clone https://github.com/xlab-si/DICE-BigData-Traffic.git
    $ cd DICE-BigData-Traffic

Next, make a temporary copy of the blueprint and the blueprint's resources:

    $ T=$(mktemp -d)
    $ chmod 755 $T
    $ cp -r blueprint/ $T

We need to update the `inputs` section of the blueprint, supplying the
private key for the VPN. Open the blueprint for editing:

    $ nano $T/blueprint/blueprint.yaml

Locate the commented out section that looks like this:

```yaml
    description: Private key of the VPN connection to Arctur
#    default: |
#      -----BEGIN PRIVATE KEY-----
#      MIIEvERYLLONGgibbrishLO0kINGtextIMITATinguuenCODEbas64privatekey
#      ...
#      Insert your key's contents here
#      ...
#      43+xNwwfueIOidf3djg2331=
#      -----END PRIVATE KEY-----

```

Remove the comment (`#`) signs, then replace the contents between the
`-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` lines with
those of the VPN's private key. Save the file and exit the editor.

Create a blueprint bundle and dispose of the temporary directory:

    $ tar -cvzf blueprint.tar.gz -C $(dirname $T) $(basename $T)
    $ rm -rf $T
    $ unset T

Finally, create and/or choose a virtual deployment container to accept the
BigData-Transport application and submit the blueprint. `$DDS_HOME` contains
path to the DICE Deployment Service's git clone location.

    $ $DDS_HOME/tools/dice-deployment-cli \
          --config $DDS_HOME/.dds.conf \
          create "DICE BigData Traffic"
    [INFO] - Checking DICE Deployment Service URL
    [INFO] - Checking DICE Deployment Service authentication data
    [INFO] - Creating new container
    d1219558-8c09-44a5-942c-5375103543cc
    [INFO] - Successfully created new container

    $ $DDS_HOME/tools/dice-deployment-cli \
          --config $DDS_HOME/.dds.conf \
          deploy d1219558-8c09-44a5-942c-5375103543cc \
          blueprint.tar.gz

[dds]:https://github.com/dice-project/DICE-Deployment-Service
[dds-cli]:https://gitlab.xlab.si/dice/DICE-deployment-service/blob/master/doc/AdminGuide.md#dice-deployment-command-line-client-configuration