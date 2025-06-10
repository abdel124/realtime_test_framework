from core.api_client import APIClient
from core.kafka_client import KafkaTestClient
import uuid

def test_rest_to_kafka_flow():
    api = APIClient("http://localhost:8000")
    kafka = KafkaTestClient()

    test_data = {
        "user_id": "u123",
        "content": "REST to Kafka test"
    }
    key = str(uuid.uuid4())

    # Send message via REST API
    response = api.send_message(**test_data)
    assert response.status_code == 200

    # Verify it reaches Kafka
    messages = kafka.consume_messages("chat-events", group_id="rest-kafka-test", expected_count=1)
    assert any(msg["content"] == "REST to Kafka test" for msg in messages)
