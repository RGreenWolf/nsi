import asyncio
import threading
import websockets
import signal
import sys
from database import User, get_session
from config import config
from utils import create_folder_if_not_exists
from web import run_flask
from ws import start_ws_server

create_folder_if_not_exists("storage")

shutdown_event = threading.Event()

def start_flask_server():
    run_flask(host=config["host"], port=config["web"]["port"], shutdown_event=shutdown_event)

async def start_websocket_server():
    await start_ws_server(config["host"], config["ws"]["port"], shutdown_event)

def run_websocket_thread():
    asyncio.run(start_websocket_server())

def stop_servers(signum, frame):
    print("Arrêt des serveurs...")
    shutdown_event.set()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_servers)

    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()

    websocket_thread = threading.Thread(target=run_websocket_thread)
    websocket_thread.start()

    flask_thread.join()
    websocket_thread.join()
