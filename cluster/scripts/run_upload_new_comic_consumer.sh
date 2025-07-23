#!/bin/bash

# ========= CONFIGURACIÓN DE RUTAS =========
FLINK_HOME="/home/hduser/flink-1.20.2"
SCRIPT_PATH="/shared/final-project-big-data/cluster/flink/upload_new_comic_consumer.py"
JAR_PATH="$FLINK_HOME/lib/flink-connector-kafka-3.4.0.jar"

# ========= ACTIVAR ENTORNO CONDA =========
# Asegúrate de haber corrido `conda init bash` antes si no funciona el activate
eval "$(conda shell.bash hook)"
conda activate pyflink310

# ========= EJECUCIÓN DE FLINK =========
$FLINK_HOME/bin/flink run \
  -py $SCRIPT_PATH \
  -pyclientexec /home/hduser/miniconda3/envs/pyflink310/bin/python \
  -pyexec /home/hduser/miniconda3/envs/pyflink310/bin/python
