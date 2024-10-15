import asyncio
import websockets
import json

# Store connected clients
connected = set()


async def handler(websocket, path):
    # Register client
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Broadcast message to all connected clients
            await broadcast(message)
    finally:
        # Unregister client
        connected.remove(websocket)


async def broadcast(message):
    for conn in connected:
        try:
            await conn.send(json.dumps({"message": message}))
        except websockets.ConnectionClosed:
            connected.remove(conn)


async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())