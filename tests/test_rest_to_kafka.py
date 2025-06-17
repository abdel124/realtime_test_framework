import pytest
from utils.api_client import APIClient
from utils.kafka_test_client import KafkaTestClient
import uuid

@pytest.mark.integration
def test_rest_to_kafka():
    api = APIClient("http://localhost:8000")
    kafka = KafkaTestClient()

    test_data = {
        "user_id": "u123",
        "content": "REST to Kafka test"
    }
    key = str(uuid.uuid4())

    response = api.send_message(**test_data)
    assert response.status_code == 200