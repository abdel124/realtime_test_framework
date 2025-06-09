import websocket
import threading
import json

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.messages = []
        self.ws = None

    def _on_message(self, ws, message):
        self.messages.append(json.loads(message))

    def _on_error(self, ws, error):
        print("WebSocket error:", error)

    def connect(self):
        self.ws = websocket.WebSocketApp(self.url,
            on_message=self._on_message,
            on_error=self._on_error
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()

    def send(self, data):
        self.ws.send(json.dumps(data))

    def close(self):
        self.ws.close()
        self.thread.join()
