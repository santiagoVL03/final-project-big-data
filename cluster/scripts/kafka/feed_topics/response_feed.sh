#!/bin/bash

# Ruta base de Kafka (ajusta si la tuya es distinta)
KAFKA_HOME="/home/santiago/kafka_2.13-3.6.2"

# Crear tópico 'responsefeed'
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --topic responsefeed \
  --bootstrap-server 10.147.20.17:9092 \
  --partitions 3 \
  --replication-factor 3

echo "Topico 'responsefeed' creado con exito."
