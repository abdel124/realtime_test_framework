from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import uvicorn

app = FastAPI()

# Allow CORS for testing from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory list of WebSocket connections
active_connections = []

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Pydantic model for incoming REST message
class MessageIn(BaseModel):
    user_id: str
    content: str

# WebSocket route
@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received from WebSocket: {data}")
            # Echo message back to client
            await websocket.send_json({"echo": data})
    except WebSocketDisconnect:
        print("Client disconnected")
        active_connections.remove(websocket)

# REST route
@app.post("/api/message")
async def handle_message(msg: MessageIn):
    message_dict = msg.dict()
    print(f"Received from REST: {message_dict}")
    # Send to Kafka
    producer.send("chat-events", value=message_dict)
    return {"status": "ok", "msg": message_dict}

# Run with: uvicorn mock_server.ws_server:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    uvicorn.run("ws_server:app", host="0.0.0.0", port=8000, reload=False)