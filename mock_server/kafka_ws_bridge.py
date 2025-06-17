import asyncio
import websockets
from kafka import KafkaConsumer
import json

connected_clients = set()

async def kafka_consumer_loop(kafka_topic):
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='ws-group'
    )
    async for message in wrap_kafka(consumer):
        await broadcast(json.dumps(message.value))

async def wrap_kafka(consumer):
    while True:
        for msg in consumer:
            yield msg

async def broadcast(message):
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

async def ws_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def main():
    ws_server = websockets.serve(ws_handler, "localhost", 8765)
    await asyncio.gather(
        ws_server,
        kafka_consumer_loop("chat-topic")
    )

if __name__ == "__main__":
    asyncio.run(main())