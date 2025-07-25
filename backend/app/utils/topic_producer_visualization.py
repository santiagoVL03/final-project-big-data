from kafka import KafkaProducer
import json

def send_visualization_message(data_dictionary: dict):
    producer = KafkaProducer(
        bootstrap_servers='10.147.20.17:9093',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    json_data = json.dumps(data_dictionary)
    print(f"JSON Data: {json_data}")

    producer.send("visualization", value=json_data)
    producer.flush()
    print("Mensaje enviado")
    
