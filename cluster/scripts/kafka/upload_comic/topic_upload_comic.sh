#!/bin/bash

# Ruta base de Kafka (ajusta si la tuya es distinta)
KAFKA_HOME="/home/santiago/kafka_2.13-3.6.2"

# Crear tópico 'uploadnewcomics'
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --topic uploadnewcomics \
  --bootstrap-server main:9092 \
  --partitions 3 \
  --replication-factor 3

echo "Topico 'uploadnewcomics' creado con exito."
