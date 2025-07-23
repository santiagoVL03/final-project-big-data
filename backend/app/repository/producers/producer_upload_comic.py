import kafka as kafka
from kafka import KafkaProducer
import json
from app.models.entities.comic import Comic

def upload_new_comic(comic_data: Comic) -> bool:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9097',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    message = {
        "data": comic_data.to_dict()
    }

    producer.send('uploadnewcomics', value=message)
    producer.flush()
    return True