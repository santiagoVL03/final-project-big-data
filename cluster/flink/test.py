from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.from_collection(["Hola", "Mundo"]).print()
env.execute("Prueba Simple")
