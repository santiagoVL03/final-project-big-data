import kafka as kafka
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import uuid

from app.models.entities.comic import Comic


def get_metadata_comics_feed(id_user: int = int(0)) -> list[Comic]:
    comics = []
    if id_user == 0:
        # Return a default feed with better options
        try:
            producer = KafkaProducer(
                bootstrap_servers='localhost:9097',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            
            correlation_id = str(uuid.uuid4())
            print('Producer created successfully')
            message = {
                "correlation_id": correlation_id,
                "id_user": id_user
            }
            producer.send('requestfeed', value=message)
            producer.flush()
            producer.close()
            consumer = KafkaConsumer(
                'responsefeed',
                group_id=f'feed_response_{id_user}',
                bootstrap_servers='localhost:9097',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print('Consumer created successfully')
            for msg in consumer:
                if msg.value.get("correlation_id") != correlation_id:
                    continue
                data_list = msg.value["data"]
                
                for data in data_list:
                    comics.append(Comic(
                        title=data.get('title', 'Default Comic'),
                        author=data.get('author', 'Unknown'),
                        description=data.get('description', 'This is a default comic description.'),
                        date_uploaded=data.get('date_uploaded', ''),
                        comic_id=data.get('comic_id', '')
                    ))
                break
        except Exception as e:
            print(f'Failed to send or receive message from Kafka: {e}')
            comics.append(Comic(
                title='Default Comic',
                author='Unknown',
                description='This is a default comic description.'
            ))
        finally:
            consumer.close()
            print('Consumer closed')
    else:
        # Return a default comic if user ID is different from 0
        # For now we do not implement a custom feed for users
        comics.append(Comic(
            title='Default Comic',
            author='Unknown',
            description='This is a default comic description.'
        ))
    return comics