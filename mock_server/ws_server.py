import asyncio
import websockets

connected_clients = set()

async def ws_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def start_ws_server():
    return await websockets.serve(ws_handler, "localhost", 8765)

if __name__ == "__main__":
    asyncio.run(start_ws_server())
