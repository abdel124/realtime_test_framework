from kafka import KafkaProducer
import json

class KafkaTestClient:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )

    def produce_message(self, topic, message, key=None):
        self.producer.send(topic, value=message, key=str(key).encode('utf-8') if key else None)
        self.producer.flush()