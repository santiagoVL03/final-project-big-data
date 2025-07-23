import kafka as kafka
from kafka import KafkaProducer
import json
from app.models.entities.comic import Comic

def upload_new_comic(comic_data: Comic) -> bool:
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9097',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print('Producer created successfully')
        message = {
            "data": comic_data.to_dict()
        }

        producer.send('uploadnewcomics', value=message)
        producer.flush()
        return True
    except Exception as e:
        print(f'Failed to send message to Kafka: {e}')
        return False
    finally:
        producer.close()
        print('Producer closed')