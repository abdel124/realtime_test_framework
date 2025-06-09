from kafka import KafkaProducer, KafkaConsumer
import json
import time

class KafkaTestClient:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, key, value):
        self.producer.send(topic, key=key.encode('utf-8'), value=value)
        self.producer.flush()

    def consume_messages(self, topic, group_id, timeout=5, expected_count=1):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='earliest',
            group_id=group_id,
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        start_time = time.time()
        messages = []

        for message in consumer:
            messages.append(message.value)
            if len(messages) >= expected_count or (time.time() - start_time) > timeout:
                break

        consumer.close()
        return messages
