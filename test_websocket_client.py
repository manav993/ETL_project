import asyncio
import websockets

async def test_client():
    uri = "ws://localhost:5678"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to server")
            while True:
                await websocket.send("Hello Server!")
                response = await websocket.recv()
                print(f"Received from server: {response}")
                await asyncio.sleep(5)  # Wait 5 seconds before sending the next message
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Disconnected from server: {e}")
        await asyncio.sleep(5)  # Wait before attempting to reconnect

asyncio.run(test_client())
