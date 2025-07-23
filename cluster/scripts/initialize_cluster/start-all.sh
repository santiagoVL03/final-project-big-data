#!/bin/bash

KAFKA_HOME=/home/hduser/kafka_2.13-3.6.2
CLUSTER_ID="W5KJ8mdcReOQyVRe9nm_1w"

for i in 1 2 3; do
  CONFIG="$KAFKA_HOME/config/kraft/broker${i}.properties"
  DATA_DIR="/tmp/kafka-logs-${i}"
  
  echo "[INFO] Formateando broker $i en $DATA_DIR"
  rm -rf "$DATA_DIR"
  "$KAFKA_HOME/bin/kafka-storage.sh" format -t "$CLUSTER_ID" -c "$CONFIG"
done

HADOOP_HOME=/home/hduser/hadoop-3.3.2
FLINK_HOME=/home/hduser/flink-1.20.2

# ========= INICIALIZACION DE FLINK =========
if ! jps | grep -q "StandaloneSessionClusterEntrypoint"; then
    echo "[INFO] Starting Flink cluster..."
    $FLINK_HOME/bin/start-cluster.sh
else
    echo "[INFO] Flink cluster is already running."
fi

# ========= INICIALIZACION DE KAFKA =========
if ! jps | grep -q "Kafka"; then
    echo "[INFO] Starting Kafka brokers..."
    for i in 1 2 3; do
        "$KAFKA_HOME/bin/kafka-server-start.sh" -daemon "$KAFKA_HOME/config/kraft/broker${i}.properties" &
    done
else
    echo "[INFO] Kafka brokers are already running."
fi

# ========= INICIALIZACION DE HDFS =========
if ! hdfs dfsadmin -report > /dev/null 2>&1; then
    echo "[INFO] Starting HDFS namenode and datanodes..."
    $HADOOP_HOME/sbin/start-all.sh
else
    echo "[INFO] HDFS is already running."
fi