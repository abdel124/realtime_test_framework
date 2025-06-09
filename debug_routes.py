from mock_server.ws_server import app
from fastapi.routing import APIRoute, APIWebSocketRoute

for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"[HTTP] Path: {route.path}, Methods: {route.methods}")
    elif isinstance(route, APIWebSocketRoute):
        print(f"[WebSocket] Path: {route.path}")
    else:
        print(f"[Other] Path: {route.path}")