from kafka import KafkaProducer
import json

def enviar_vista_kafka(user_id: str, comic_id: str) -> bool:
    try:
        producer = KafkaProducer(
            bootstrap_servers='nifla:9097',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        message = {
            "user_id": user_id,
            "comic_id": comic_id
        }
        print(f"Enviando mensaje a Kafka: {message}")
        producer.send('comic_visitas', value=message)
        producer.flush()
        return True
    except Exception as e:
        print(f"Kafka error: {e}")
        return False
    finally:
        producer.close()
