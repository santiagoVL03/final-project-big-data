#!/bin/bash

# Ruta base de Kafka (ajusta si la tuya es distinta)
KAFKA_HOME="/home/nifla/kafka_2.13-3.6.2"

# Crear tópico 'uploadnewcomics'
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --topic comic_visitas \
  --bootstrap-server nifla:9097 \
  --partitions 3 \
  --replication-factor 3

echo "Topico 'uploadnewcomics' creado con exito."