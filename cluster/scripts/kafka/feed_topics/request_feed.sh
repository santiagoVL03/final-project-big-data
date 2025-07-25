#!/bin/bash

# Ruta base de Kafka (ajusta si la tuya es distinta)
KAFKA_HOME="/home/santiago/kafka_2.13-3.6.2"

# Crear tópico 'requestfeed'
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --topic requestfeed \
  --bootstrap-server 10.147.20.17:9092 \
  --partitions 3 \
  --replication-factor 3

echo "Topico 'requestfeed' creado con exito."
