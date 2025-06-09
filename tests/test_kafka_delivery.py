from core.kafka_client import KafkaTestClient
import uuid

def test_kafka_message_delivery():
    topic = "chat-events"
    group_id = "chat-test-group"
    kafka = KafkaTestClient()

    test_msg = {
        "user_id": "test-user",
        "content": "Kafka message test",
        "timestamp": "2025-06-09T10:00:00Z"
    }

    key = str(uuid.uuid4())
    kafka.send_message(topic, key, test_msg)

    messages = kafka.consume_messages(topic, group_id, expected_count=1)

    assert any(msg["content"] == "Kafka message test" for msg in messages)