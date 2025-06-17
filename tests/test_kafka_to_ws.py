import asyncio
import pytest
from utils.kafka_test_client import KafkaTestClient
from utils.websocket_test_client import WebSocketTestClient
import uuid

@pytest.mark.asyncio
async def test_kafka_to_websocket_broadcast():
    kafka = KafkaTestClient()
    ws_client = WebSocketTestClient()

    test_data = {
        "user_id": "u456",
        "content": "Kafka to WebSocket test"
    }
    key = str(uuid.uuid4())

    kafka.produce_message("chat-topic", test_data, key=key)
    received = await ws_client.listen(expected_count=1)

    assert any(msg["content"] == "Kafka to WebSocket test" for msg in received)