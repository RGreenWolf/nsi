import asyncio
import websockets

async def client():
    uri = "ws://localhost:5500"
    async with websockets.connect(uri) as websocket:
        message = "Bonjour serveur!"
        await websocket.send(message)
        print(f"Message envoyé : {message}")
        
        try:
            while True:
                response = await websocket.recv()
                print(f"Réponse reçue : {response}")
        except websockets.ConnectionClosed:
            print("Connexion fermée par le serveur.")

def start_ws():
    asyncio.get_event_loop().run_until_complete(client())
