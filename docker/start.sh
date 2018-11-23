#!/bin/bash

# export PYSPARK_DRIVER_PYTHON=jupyter
# export PYSPARK_DRIVER_PYTHON_OPTS='notebook'
# export PYSPARK_PYTHON="python3"
# pyspark --conf 'spark.debug.maxToStringFields=1000' --conf "spark.executorEnv.PYTHONHASHSEED": "0" 

nohup jupyter notebook--ip=0.0.0.0 --no-browser --NotebookApp.token='test' --NotebookApp.iopub_data_rate_limit=10000000000 --allow-root &

