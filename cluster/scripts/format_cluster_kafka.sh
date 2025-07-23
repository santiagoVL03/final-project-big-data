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

