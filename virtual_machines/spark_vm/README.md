## Apache Spark

The flowing guide for setting up a spark cluster is provided by 
[Tadej Borovsak](https://gitlab.xlab.si/tadej.borovsak/local-spark).

#### Setting up cluster

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

[chef-repo]: https://gitlab.xlab.si/dice/dice-chef-repo
[spark-ui]: http://192.168.0.62:8080