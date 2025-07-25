#!/bin/bash

KAFKA_HOME=/home/santiago/kafka_2.13-3.6.2
CLUSTER_ID="W5KJ8mdcReOQyVRe9nm_1w"

CONFIG="$KAFKA_HOME/config/kraft/broker.properties"
DATA_DIR="/tmp/kafka-logs"

echo "[INFO] Formateando broker en $DATA_DIR"

rm -rf "$DATA_DIR"


"$KAFKA_HOME/bin/kafka-storage.sh" format -t "$CLUSTER_ID" -c "$CONFIG"

HADOOP_HOME=/home/santiago/hadoop-3.3.2
FLINK_HOME=/home/santiago/flink-1.20.2

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
    "$KAFKA_HOME/bin/kafka-server-start.sh" -daemon "$KAFKA_HOME/config/kraft/broker.properties" &
else
    echo "[INFO] Kafka brokers are already running."
fi

# ========= INICIALIZACION DE HDFS =========
if ! hdfs dfsadmin -report > /dev/null 2>&1; then
    echo "[INFO] Starting HDFS namenode and datanodes..."
    $HADOOP_HOME/sbin/start-dfs.sh
else
    echo "[INFO] HDFS is already running."
fi