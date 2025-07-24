from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    kafka_props = {
        'bootstrap.servers': 'main:9097',
        'group.id': 'flink-upload-new-comic-consumer'
    }

    consumer = FlinkKafkaConsumer(
        topics='uploadnewcomics',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    ds = env.add_source(consumer).map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    from pyflink.common import Row
    from pyflink.datastream.functions import MapFunction
    
    class ExtractComic(MapFunction):
        def map(self, value):
            data = value.get("data", {})
            return Row(data.get("author", ""), data.get("title", ""), data.get("description", ""), data.get("date_uploaded", ""), data.get("comic_id", ""))

    typed_stream = ds.map(ExtractComic(), output_type=Types.ROW([
        Types.STRING(),  # author
        Types.STRING(),  # title
        Types.STRING(),  # description
        Types.STRING(),  # date_uploaded
        Types.STRING()   # comic_id
    ]))

    table = t_env.from_data_stream(
        typed_stream,
        col("f0").alias("author"),
        col("f1").alias("title"),
        col("f2").alias("description"),
        col("f3").alias("date_uploaded"),
        col("f4").alias("comic_id")
    )

    t_env.create_temporary_view("comics_view", table)

    t_env.execute_sql("""
        CREATE TABLE comics (
            author STRING,
            title STRING,
            description STRING,
            date_uploaded STRING,
            comic_id STRING
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://10.147.20.121:5432/comics_bd',
            'table-name' = 'comics',
            'username' = 'postgres',
            'password' = '1234',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    t_env.execute_sql("INSERT INTO comics SELECT * FROM comics_view")
main()

# How to run:

"""
  /home/hduser/flink-1.20.2/bin/flink run \
  -py /shared/final-project-big-data/cluster/flink/upload_comic/upload_new_comic_flink.py \
  -pyclientexec /home/hduser/miniconda3/envs/pyflink310/bin/python \
  -pyexec /home/hduser/miniconda3/envs/pyflink310/bin/python
"""
