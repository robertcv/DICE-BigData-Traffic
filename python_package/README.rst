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

Additionally you have to set some environment variables or have a
``local_settings.py`` file. All settings can be found in ``settings.py``.

Set at least those variables:

.. code:: bash

    $ export TIMON_USERNAME=user
    $ export TIMON_PASSWORD=password

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

    $ export KAFKA_HOST=127.0.0.1
    $ export KAFKA_PORT=9092
    $ pytraffic --bt_collector --il_collector --pollution_collector

This takes Kafka host and port as defined with ``KAFKA_HOST`` and ``KAFKA_PORT``
environment variables. It then runs bluetooth sensors, inductive loops and air
pollution collectors.

.. code:: bash

    $ export BT_SENSORS_IMG_DIR=/home/user/image
    $ pytraffic --kafka 127.0.0.1:9092 --bt_collector --plot bt

This sets Kafka host to 127.0.0.1 and port to 9092. It then sends bluetooth data
to Kafka. Finally it saves a plot of sensors location into the directory
specified with ``BT_SENSORS_IMG_DIR``. Warning: as for now to just plot data you
still have to have a working Kafka.
