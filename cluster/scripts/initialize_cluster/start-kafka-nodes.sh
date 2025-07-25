KAFKA_HOME=/home/santiago/kafka_2.13-3.6.2
CLUSTER_ID="W5KJ8mdcReOQyVRe9nm_1w"

CONFIG="$KAFKA_HOME/config/kraft/broker.properties"
DATA_DIR="/tmp/kafka-logs"

echo "[INFO] Formateando broker en $DATA_DIR"

rm -rf "$DATA_DIR"


"$KAFKA_HOME/bin/kafka-storage.sh" format -t "$CLUSTER_ID" -c "$CONFIG"

if ! jps | grep -q "Kafka"; then
    echo "[INFO] Starting Kafka brokers..."
    "$KAFKA_HOME/bin/kafka-server-start.sh" -daemon "$KAFKA_HOME/config/kraft/broker.properties" &
else
    echo "[INFO] Kafka brokers are already running."
fi