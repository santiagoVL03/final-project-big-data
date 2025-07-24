from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='main:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {"usuario": "santi", "comic": "El Señor de la Duna"}

producer.send("likescomics", value=data)
producer.flush()
print("Mensaje enviado")
