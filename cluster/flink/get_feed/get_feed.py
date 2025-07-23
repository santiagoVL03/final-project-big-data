from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json
import random
from kafka import KafkaProducer
from hdfs import InsecureClient

def read_metadata_from_hdfs() -> list[dict]:
    """
    Retorna una lista de metadatas en JSON desde rutas aleatorias usando el cliente HDFS.
    """
    try:
        # Ajusta el hostname y puerto si es necesario
        client = InsecureClient('http://localhost:9870', user='hduser')

        comic_paths = client.list('/comics', status=False)  # solo nombres, sin detalles
        if not comic_paths:
            return [{"error": "No hay cómics en HDFS"}]

        selected_ids = random.sample(comic_paths, min(5, len(comic_paths)))

        metadatas = []
        for comic_id in selected_ids:
            path = f"/comics/{comic_id}/metadata"
            with client.read(path, encoding='utf-8') as reader:
                reader = json.JSONDecoder()
                metadata = json.load(reader) # type: ignore
                metadatas.append(metadata)

        return metadatas

    except Exception as e:
        return [{"error": f"Error al leer HDFS: {str(e)}"}]

def send_response_to_kafka(correlation_id, user_id) -> None:
    """
    Envia la metadata al tópico 'responsefeed'
    """
    producer = KafkaProducer(
        bootstrap_servers='localhost:9097',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    metadatas = read_metadata_from_hdfs()

    message = {
        "correlation_id": correlation_id,
        "id_user": user_id,
        "comics_metadata": metadatas
    }

    producer.send("responsefeed", message)
    producer.flush()
    producer.close()

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    kafka_props = {
        'bootstrap.servers': 'localhost:9097',
        'group.id': 'flink-upload-new-comic-consumer'
    }

    consumer = FlinkKafkaConsumer(
        topics='requestfeed',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    ds = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    from pyflink.common import Row
    from pyflink.datastream.functions import MapFunction

    class ProcessRequest(MapFunction):
        def map(self, value):
            data = value.get("data", {})
            correlation_id = data.get("correlation_id", "")
            id_user = data.get("id_user", "")

            # Llama a función que lee metadata y la publica en Kafka
            send_response_to_kafka(correlation_id, id_user)

            return Row(correlation_id, id_user)

    typed_stream = ds.map(ProcessRequest(), output_type=Types.ROW([
        Types.STRING(),  # correlation_id
        Types.STRING()   # id_user
    ]))

    env.execute("Get Feed Flink Job")

if __name__ == "__main__":
    main()


# How to run:

"""
  /home/hduser/flink-1.20.2/bin/flink run \
  -py /shared/final-project-big-data/cluster/flink/get_feed/get_feed.py \
  -pyclientexec /home/hduser/miniconda3/envs/pyflink310/bin/python \
  -pyexec /home/hduser/miniconda3/envs/pyflink310/bin/python
"""

"""
   For testing you can create a custom consumer script that sends a request to the 'requestfeed' topic.
    Example:
    /home/hduser/kafka_2.13-3.5.1/bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9097 \
    --topic requestfeed \

"""