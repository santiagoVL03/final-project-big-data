#!/bin/bash

# Ruta base de Kafka (ajusta si la tuya es distinta)
KAFKA_HOME="/home/santiago/kafka_2.13-3.6.2"

# Crear tópico 'likestopic'
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --topic likestopic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 3

echo "Tópico 'likestopic' creado con éxito."
