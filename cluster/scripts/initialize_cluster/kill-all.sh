#!/bin/bash

PROCESOS=(
  "NameNode"
  "DataNode"
  "SecondaryNameNode"
  "ResourceManager"
  "NodeManager"
  "Kafka"
  "TaskManagerRunner"
  "StandaloneSessionClusterEntrypoint"
)

echo "Matando procesos relacionados con Hadoop, Kafka y Flink..."

for nombre in "${PROCESOS[@]}"; do
  echo "Buscando proceso: $nombre"
  pids=$(jps | grep "$nombre" | awk '{print $1}')
  for pid in $pids; do
    echo "Matando $nombre con PID $pid"
    kill -9 "$pid"
  done
done

echo "Todos los procesos relevantes han sido terminados."
