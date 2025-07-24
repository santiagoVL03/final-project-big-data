from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json

def main():
    # Crear entornos de ejecución
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Propiedades de Kafka
    kafka_props = {
        'bootstrap.servers': '10.147.20.191:9097',  # IP real del broker Kafka
        'group.id': 'flink-like-consumer'
    }

    # Crear consumidor Kafka
    consumer = FlinkKafkaConsumer(
        topics='likestopic',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # Convertir el string JSON en dict de Python
    ds = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    # Extraer campos relevantes usando MapFunction
    from pyflink.common import Row
    from pyflink.datastream.functions import MapFunction

    class ExtractLike(MapFunction):
        def map(self, value):
            return Row(value.get("usuario", ""), value.get("comic_id", ""), value.get("nombre_comic", ""))

    # Transformar el stream a tipos conocidos
    typed_stream = ds.map(ExtractLike(), output_type=Types.ROW([
        Types.STRING(),  # usuario
        Types.STRING(),  # comic_id
        Types.STRING()   # nombre_comic
    ]))

    # Convertir el DataStream a tabla
    table = t_env.from_data_stream(
        typed_stream,
        col("f0").alias("usuario"),
        col("f1").alias("comic_id"),
        col("f2").alias("nombre_comic")
    )

    # Crear vista temporal
    t_env.create_temporary_view("likes_view", table)

    # Crear tabla JDBC en PostgreSQL
    t_env.execute_sql("""
        CREATE TABLE comics_likes (
            usuario STRING,
            comic_id STRING,
            nombre_comic STRING
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://10.147.20.121:5432/comics_bd',
            'table-name' = 'comics_likes',
            'username' = 'postgres',
            'password' = '1234',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    # Insertar los datos en la tabla de PostgreSQL
    t_env.execute_sql("INSERT INTO comics_likes SELECT * FROM likes_view")

main()

"""
  /home/hduser/flink-1.20.2/bin/flink run \
  -py /shared/final-project-big-data/cluster/flink/get_feed/get_feed.py \
  -pyclientexec /home/hduser/miniconda3/envs/pyflink310/bin/python \
  -pyexec /home/hduser/miniconda3/envs/pyflink310/bin/python
"""