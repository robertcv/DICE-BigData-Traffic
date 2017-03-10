# Setting up local Apache Spark cluster using Vagrant

This is a short guide on setting up local development cluster.


## Cluster contents

By default, cluster is composed of:

  * Apache Spark master node at 192.168.0.62 and
  * two Apache Spark worker nodes at 192.168.0.6{3,4}


## Setting up cluster

First thing we need to do is to clone this repo somewhere and move into it.
Next, clone [dice-chef-repo][chef-repo] and create new empty folder `nodes`.
For the lazy devs, this sequence of commands should do the trick:

    $ cd
    $ git clone ssh://git@gitlab.xlab.si:13022/tadej.borovsak/local-spark.git
    $ cd local-spark
    $ mkdir nodes
    $ git clone ssh://git@gitlab.xlab.si:13022/dice/dice-chef-repo.git \
        --branch develop

Now simply run `vagrant up` and wait.

Because Chef is not the smartest kid on the block when it comes to ip address
management, we need to do a few things on our own. Run `vagrant ssh master`,
then `sudo vim /etc/spark/spark-env.sh` and make this file look like this
(edit last two lines):

    # Auto-enerated by Chef. DO NOT MODIFY MANUALLY
    SPARK_CONF_DIR="/etc/spark"
    SPARK_LOG_DIR="/var/log/spark"
    SPARK_IDENT_STRING="default_ident"
    SPARK_MASTER_PORT="7077"
    SPARK_WORKER_PORT="7078"
    SPARK_WORKER_DIR="/var/lib/spark/"
    SPARK_LOCAL_IP="192.168.0.62"
    SPARK_MASTER_HOST="192.168.0.62"

Save file and run `sudo start spark-master`. Now visit [Spark UI][spark-ui]
and confirm that master is up and running.

Next, we need to spin up workers. Execute `vagrant ssh worker-3` and then edit
`/etc/spark/spark-env.sh` to this:

    # Auto-enerated by Chef. DO NOT MODIFY MANUALLY
    SPARK_CONF_DIR="/etc/spark"
    SPARK_LOG_DIR="/var/log/spark"
    SPARK_IDENT_STRING="default_ident"
    SPARK_MASTER_PORT="7077"
    SPARK_WORKER_PORT="7078"
    SPARK_WORKER_DIR="/var/lib/spark/"
    SPARK_LOCAL_IP="192.168.0.63"
    SPARK_MASTER_HOST="192.168.0.62"

Save file and run `sudo start spark-worker`. Now visit [Spark UI][spark-ui]
again and confirm that new worker can be seen by master. Now repeat the same
thing for worker-4, just make sure to replace `192.168.0.63` with
`192.168.0.64`.

[chef-repo]: ssh://git@gitlab.xlab.si:13022/dice/dice-chef-repo.git
[spark-ui]: http://192.168.0.62:8080


## Testing if things really work

Login to master VM using `vagrant ssh master` and then execute

    $ /usr/share/spark-2.0.0-bin-hadoop2.7/bin/spark-shell \
        --master spark://192.168.0.62:7077

This should start scala REPL and Spark web UI should show one application that
took all of the resources from cluster.


## Final remarks

Feel free to modify vagrant file with additional Chef recipes that
automatically install monitoring agent. Any contribution in that direction
will make it easier to add this functionality into final product.
