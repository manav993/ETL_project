import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            if message == "ping":
                print(f"Received keep-alive ping from {websocket.remote_address}")
                await websocket.pong()  # Respond with a pong if you are expecting to handle ping/pong
                continue  # Ignore the ping message
            print(f"Received message from client: {message}")
            await websocket.send(message)  # Echo message back to client
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client disconnected unexpectedly: {e}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Client closed connection normally.")
    finally:
        connected_clients.remove(websocket)
        print(f"Client removed: {websocket.remote_address}")

async def main():
    server = await websockets.serve(
        handler,
        "localhost",
        5678,
        ping_timeout=120,  # Increase ping timeout to 120 seconds
        close_timeout=60   # Increase close timeout to 60 seconds
    )
    await server.wait_closed()

asyncio.run(main())
