from pyflink.common import Configuration, Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json

def main():
    config = Configuration()
    config.set_string(
        "pipeline.jars",
        ":".join([
            "file:///home/hduser/flink-1.20.2/lib/flink-connector-kafka-3.4.0.jar",
            "file:///home/hduser/flink-1.20.2/opt/flink-python-1.20.2.jar",
            "file:///home/hduser/flink-1.20.2/opt/py4j-0.10.9.7.jar"
        ])
    )

    env = StreamExecutionEnvironment.get_execution_environment(configuration=config)

    kafka_props = {
        'bootstrap.servers': 'localhost:9093',
        'group.id': 'flink-upload-new-comic-consumer'
    }

    consumer = FlinkKafkaConsumer(
        topics='uploadnewcomics',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    stream = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.PICKLED_BYTE_ARRAY())

    stream.map(lambda x: f"Usuario: {x['user']} subió un nuevo cómic: {x['comic']}").print()

    env.execute("Kafka Upload New Comic Consumer")

if __name__ == '__main__':
    main()
