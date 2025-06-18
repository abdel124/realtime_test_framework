import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketTestClient:
    def __init__(self, uri="ws://localhost:8765"):
        self.uri = uri
        self.received_messages = []

    async def listen(self, expected_count=1, timeout=5):
        try:
            async with websockets.connect(self.uri) as websocket:
                logger.info(f"Connected to WebSocket server at {self.uri}")
                for _ in range(expected_count):
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout)
                        logger.info(f"Received message: {message}")
                        self.received_messages.append(json.loads(message))
                    except asyncio.TimeoutError:
                        logger.warning("Timeout while waiting for WebSocket message")
                        break
        except Exception as e:
            logger.error(f"Failed to connect or receive from WebSocket: {e}")

        return self.received_messages
