import streamlit as st
import asyncio
import websockets
import json

# Function to fetch data from WebSocket
async def fetch_data():
    uri = "ws://localhost:5678"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")
            message = await websocket.recv()
            return json.loads(message)
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")
        return []

# Function to update Streamlit UI with fetched data
async def update_data():
    st.title('Real-Time WebSocket Data')
    data_display = st.empty()

    while True:
        data = await fetch_data()
        if data:
            data_display.write(data)
        await asyncio.sleep(1)  # Adjust the frequency of updates as needed

# Run the asynchronous function using asyncio
asyncio.run(update_data())
