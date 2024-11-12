# ws.py
import asyncio
import websockets
from database import get_session, User
import requests 

async def handle_connection(websocket, path):
    async def send_server_messages():
        while True:
            server_message = await asyncio.to_thread(input, "Message à envoyer aux clients: ")
            await websocket.send(f"Serveur: {server_message}")

    asyncio.create_task(send_server_messages())

    async for message in websocket:
        print(f"Message reçu de client: {message}")
        await websocket.send(message)

async def start_ws_server(host, port, shutdown_event):
    server = await websockets.serve(handle_connection, host, port)
    print(f"Serveur WebSocket démarré sur ws://{host}:{port}")

    try:
        while not shutdown_event.is_set():
            await asyncio.sleep(0.1)
    finally:
        server.close()
        await server.wait_closed()
        print("Serveur WebSocket arrêté.")