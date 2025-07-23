from pyflink.common import Configuration, Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json

def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    kafka_props = {
        'bootstrap.servers': 'localhost:9097',
        'group.id': 'flink-upload-new-comic-consumer'
    }

    # Crear el consumer
    consumer = FlinkKafkaConsumer(
        topics='uploadnewcomics',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # Deserializa el JSON a diccionario
    stream = env.add_source(consumer).map(
        lambda x: json.loads(x),
        output_type=Types.MAP(Types.STRING(), Types.STRING())  # Este es superficial, porque JSON anidado no cabe bien acá
    )

    # Imprime autor y título desde el campo 'data'
    stream.map(
        lambda x: f"Autor: {x['data']['author']} subió el cómic: {x['data']['title']}"
    ).print()

    env.execute("Kafka Upload New Comic Consumer")
main()

# How to run:

"""
  /home/hduser/flink-1.20.2/bin/flink run \
  -py /shared/final-project-big-data/cluster/flink/upload_new_comic_consumer.py \
  -pyclientexec /home/hduser/miniconda3/envs/pyflink310/bin/python \
  -pyexec /home/hduser/miniconda3/envs/pyflink310/bin/python
"""
