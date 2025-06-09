import websocket
import threading
import json
import time

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.messages = []
        self.ws = None
        self.thread = None

    def _on_message(self, ws, message):
        print("[WebSocket] Received:", message)
        self.messages.append(json.loads(message))

    def _on_error(self, ws, error):
        print("[WebSocket] Error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("[WebSocket] Closed:", close_status_code, close_msg)

    def _on_open(self, ws):
        print("[WebSocket] Connection opened")

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

        # Wait until connection is established
        time.sleep(2)

    def send(self, data):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(json.dumps(data))
        else:
            raise RuntimeError("WebSocket is not connected")

    def close(self):
        self.ws.close()
        if self.thread:
            self.thread.join()