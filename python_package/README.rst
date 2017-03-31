Pytraffic python module
-----------------------

This module combines collectors of traffic data in Ljubljana and forwards it to
given Kafka node. It comes with a CLI tool called ``pytraffic``. This enables
control over which collector is being used. This can be specified with
arguments.

For more information on them use:

.. code:: bash

    $ pytraffic --help

    usage: pytraffic [-h] [--kafka KAFKA] [--bt_collector] [--counters_collector]
                     [--il_collector] [--pollution_collector]
                     [--lpp_collector [{station,static,live} [{station,static,live} ...]]]
                     [--plot [{bt,counters,il} [{bt,counters,il} ...]]]
                     [--config CONFIG]

    optional arguments:
      -h, --help            show this help message and exit
      --kafka KAFKA         Kafka bootstrap server address in format hostname:port
      --bt_collector        Start bluetooth collector
      --counters_collector  Start counters collector
      --il_collector        Start inductive loops collector
      --pollution_collector
                            Start pollution collector
      --lpp_collector [{station,static,live} [{station,static,live} ...]]
                            Start lpp collector
      --plot [{bt,counters,il} [{bt,counters,il} ...]]
                            Plot map
      --config CONFIG       Configuration file to use


Additionally you have to create a configuration file that's in JSON format. This
overrides the default settings set in ``config.py``. For ``pytraffic`` to fully
work you have to have set at least those settings:

.. code:: bash

    $ cat local.conf
    {
        "kafka_host": "127.0.0.1:9092",
        "bt_sensors": {
            "timon_username": "username",
            "timon_password": "password",
            "timon_crt_file": "datacloud.crt"
        }
    }


If you want to plot maps of collectors location you have to install additional
requirements. Use:

.. code:: bash

    $ pip install -r requirements-plot.txt`


Some examples
~~~~~~~~~~~~~

.. code:: bash

    $ pytraffic --kafka 127.0.0.1:9092 --lpp_collector static live

This sets Kafka host to 127.0.0.1 and port to 9092. It then runs lpp collector
which sends static and live arrival times to Kafka.

.. code:: bash

    $ cat local.conf
    {
        "kafka_host": "127.0.0.1:9092",
        "bt_sensors": {
            "timon_username": "username",
            "timon_password": "password",
            "timon_crt_file": "datacloud.crt"
        }
    }
    $ pytraffic --bt_collector --il_collector --pollution_collector

This runs bluetooth sensors, inductive loops and air pollution collectors. Note:
because we saved configurations in a ``local.conf`` file, ``pytraffic``
automatically loads it and we don't have to specify the ``--config`` argument.

.. code:: bash

    $ cat conf/pytraffic.conf
    {
        "kafka_host": "127.0.0.1:9092",
        "inductive_loops": {
            "img_dir": "/home/user/image"
        }
    }
    $ pytraffic --il_collector --plot il --config conf/pytraffic.conf

This loads configurations from ``conf/pytraffic.conf`` and runs inductive loops
collector. It also generates a plot of inductive loops location and saves it
into the directory set in ``img_dir``. Warning: as for now to just plot data you
still have to have a working Kafka.
