## Spark

* Run Apache Spark locally:

```bash
export SPARK_HOME=/home/ubuntu/spark-2.0.1-bin-hadoop2.7
./run_spark_local.py app.py
```

* To run it on cluster execute this (on master):

```bash
./run_spark_clouster.py spark://hostname:7077 app.py
```

* Test it locally with ipython notebooks:
    
```bash
export SPARK_HOME=/home/ubuntu/spark-2.0.1-bin-hadoop2.7
cd ipython_notebooks/
./run_pyspark.sh
```