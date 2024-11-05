import threading
from flask import Flask, request, jsonify
import uuid
import random
import json
import os
import hashlib

app = Flask(__name__)

def load_data(file_name): 
    file_name = "data/" + file_name
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    return {}

def save_data(file_name, data):
    file_name = "data/" + file_name
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def commande():
    sa = 0

threadCmd = threading.Thread(target=commande)

def startServer():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

threadWeb = threading.Thread(target=startServer)

if __name__ == '__main__':
    threadWeb.start()
    threadCmd.start()

