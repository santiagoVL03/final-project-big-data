from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
import json

def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    kafka_props = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'flink-likes-consumer'
    }

    # Crea el consumidor Kafka
    consumer = FlinkKafkaConsumer(
        topics='likescomics',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    stream = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.PICKLED_BYTE_ARRAY())

    # Para efectos de demostración, simplemente imprime los datos
    stream.map(lambda x: f"Usuario: {x['user']} dio like a {x['comic']}").print()

    env.execute("Kafka Likes Consumer")

if __name__ == '__main__':
    main()
