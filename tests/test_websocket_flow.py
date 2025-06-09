from core.websocket_client import WebSocketClient
import time

def test_ws_message_exchange():
    ws = WebSocketClient("ws://localhost:8000/ws/chat")
    ws.connect()

    test_data = {"user_id": "test1", "content": "hello"}
    ws.send(test_data)

    time.sleep(2)  # give server time to respond
    ws.close()

    assert any(m["content"] == "hello" for m in ws.messages)
