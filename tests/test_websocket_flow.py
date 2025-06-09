from core.websocket_client import WebSocketClient
import time

def test_ws_message_exchange():
    ws = WebSocketClient("ws://localhost:8000/ws/chat")
    ws.connect()

    test_data = {"user_id": "test1", "content": "hello"}
    ws.send(test_data)

    time.sleep(2)
    ws.close()
    print("All received messages:", ws.messages)

    # ✅ Fix: Check nested structure under "echo"
    assert any("echo" in m and m["echo"]["content"] == "hello" for m in ws.messages)
