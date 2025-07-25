from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json
from datetime import datetime

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    kafka_props = {
        'bootstrap.servers': 'nifla:9097',
        'group.id': 'flink-vistas-comic-consumer'
    }

    consumer = FlinkKafkaConsumer(
        topics='comic_visitas',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    ds = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    from pyflink.common import Row
    from pyflink.datastream.functions import MapFunction

    class ExtractVista(MapFunction):
        def map(self, value):
            return Row(
                value.get("user_id", ""),
                value.get("comic_id", ""),
                datetime.now().isoformat()  # fecha actual
            )

    typed_stream = ds.map(ExtractVista(), output_type=Types.ROW([
        Types.STRING(),  # user_id
        Types.STRING(),  # comic_id
        Types.STRING()   # fecha (ISO)
    ]))

    table = t_env.from_data_stream(
        typed_stream,
        col("f0").alias("user_id"),
        col("f1").alias("comic_id"),
        col("f2").alias("fecha")
    )

    t_env.create_temporary_view("vistas_view", table)

    t_env.execute_sql("""
        CREATE TABLE vistas_comics (
            user_id STRING,
            comic_id STRING,
            fecha STRING
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://main:5432/comics_bd',
            'table-name' = 'vistas_comics',
            'username' = 'postgres',
            'password' = '1234',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    t_env.execute_sql("INSERT INTO vistas_comics SELECT * FROM vistas_view")

main()
'''
//// run flink
flink run \
  -py /home/nifla/GITHUB/final-project-big-data/cluster/flink/vistas_comic/vistas_comic_flink.py \
  -pyclientexec ~/miniconda3/envs/pyflink310/bin/python \
  -pyexec ~/miniconda3/envs/pyflink310/bin/python

'''
        
'''
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common import Row
from pyflink.datastream.functions import MapFunction

import json
from datetime import datetime

def main():
    print("✅ Iniciando Job Flink para vistas_comic")

    # Crear entornos
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Configuración Kafka
    kafka_props = {
        'bootstrap.servers': 'nifla:9097',
        'group.id': 'flink-vistas-comic-consumer'
    }

    consumer = FlinkKafkaConsumer(
        topics='comic_visitas',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # Deserialización y debug
    ds = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    class ExtractVista(MapFunction):
        def map(self, value):
            print("📥 Mensaje recibido desde Kafka:", value)

            user_id = value.get("user_id", "anonimo")
            comic_id = value.get("comic_id", "desconocido")
            fecha = datetime.now().isoformat()

            print(f"🧾 Enviando Row: user_id={user_id}, comic_id={comic_id}, fecha={fecha}")
            return Row(user_id, comic_id, fecha)

    typed_stream = ds.map(ExtractVista(), output_type=Types.ROW([
        Types.STRING(),  # user_id
        Types.STRING(),  # comic_id
        Types.STRING()   # fecha
    ]))

    # Convertir a tabla
    table = t_env.from_data_stream(
        typed_stream,
        col("f0").alias("user_id"),
        col("f1").alias("comic_id"),
        col("f2").alias("fecha")
    )

    t_env.create_temporary_view("vistas_view", table)

    # Crear tabla en PostgreSQL (si no existe)
    t_env.execute_sql("""
        CREATE TABLE IF NOT EXISTS vistas_comics (
            user_id STRING,
            comic_id STRING,
            fecha STRING
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://main:5432/comics_bd',
            'table-name' = 'vistas_comics',
            'username' = 'postgres',
            'password' = '1234',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    # Ejecutar INSERT con espera explícita
    print("🚀 Ejecutando INSERT INTO vistas_comics SELECT * FROM vistas_view")
    result = t_env.execute_sql("INSERT INTO vistas_comics SELECT * FROM vistas_view")
    result.wait()
    print("✅ Inserción finalizada o en espera de más datos.")

main()

'''