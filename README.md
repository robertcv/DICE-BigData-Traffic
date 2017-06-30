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

# Testing the project in Jenkins

## Validation of the `develop` branch

Testing the `develop` branch is a good practice, which lets us automatically
validate the internally stable but not yet fully tested commits. Typically we
want them to be run shortly after someone merges the changes to this branch
and pushes them to a common repository (such as github or gitlab).

This project contains a `Jenkinsfile` in the repository root, which runs two
stages: a unit test stage, testing the Python code logic, and a kitchen test
stage, testing the Chef recipes. The definition file assumes that Jenkins has
a node named `master`, where the Python tests can run. It also needs to have
a remote node named `dice_worker`, which has to reside somewhere where kitchen
can provision and destroy virtual machines as needed.

The steps in the `Jenkinsfile` then assume that a `kitchen.local.yml` file is
present in the `workspace` folder of the worker Jenkins folder. See
[misc/.kitchen.local.yml] for an example. Of course the Jenkins node has to
assign in its settings all the environment variables that are used in the
`.kitchen.local.yml` file.

To create a `develop` branch validation project in Jenkins, create a pipeline
project. It should be enough to use definition of pipeline script from SCM and
name Script Path as `Jenkinsfile`.

This scenario works if both the  `master` and the `dice_worker` Jenkins nodes
can reach the SCM on the same address.

## Validation from Gerrit

It is greatly convenient if the Gerrit review process also uses Jenkins to
verify the code. In principle, the same approach as for validating the
`develop` branch might work. But in our organization, Gerrit has been located
out of reach of `dice_worker`. Considering that the previous approach does
a SCM fetch on both nodes, this doesn't work.

Instead, we prepared `Jenkins-imperative`. This definition mandates a different
way of populating the satellite node's workspace (using stash in the pipeline).

Like before, create a Pipeline project in Jenkins. Then ensure the following
items are set:

* Build Triggers: Gerrit event must be checked
* Gerrit Trigger:
  * Click Advanced and populate Gerrit Reporting Values as needed (e.g.,
    Verify Successful 1, Verify Failed -1).
  * In Gerrit Project, set the pattern for your project in Gerrit that
    represents this repository. Also set the branch pattern to the one
    used in Gerrit's project.
* Pipeline
  * Definition: Pipeline script from SCM
  * SCM: Git
  * Repositories:
    * Repository URL is the URL to your Gerrit's Git interface, e.g.,
      `ssh://jenkins@gerrit2.local.lan:29418/BigData-Transport`
    * Click Advanced
    * Refspec: `$GERRIT_REFSPEC`
    * Branches to build: `$GERRIT_BRANCH`
    * Additional Behaviours: click Add and pick Strategy for choosing what to build
      * Choosing strategy: Gerrit Trigger (if you don't pick this, Jenkins will
        always check out a parent of the target branch, e.g., `develop`)
  * Script Path: `Jenkins-imperative`
  * Lightweight checkout must **not** be selected (otherwise you'll get errors
    that `$GERRIT_REFSPEC` and `$GERRIT_BRANCH` are unknown branches, because
    they variables will not be assigned their values.)

You will probably notice that the Git settings together with the Gerrit Trigger
are a bit redundant, because this will only affect the Jenkins accessing the
`Jenkinsfile`. It is quite possible that the SCM sync will happen on a
non-master node, so it might start executing the pipeline on a node that has
not received the updated code. See Pipeline Jobs in [Gerrit Trigger
documentation].

[dds]:https://github.com/dice-project/DICE-Deployment-Service
[dds-cli]:https://gitlab.xlab.si/dice/DICE-deployment-service/blob/master/doc/AdminGuide.md#dice-deployment-command-line-client-configuration
[Gerrit Trigger documentation]:https://wiki.jenkins.io/display/JENKINS/Gerrit+Trigger