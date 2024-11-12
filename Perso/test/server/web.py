# server.py
from flask import Flask, jsonify, request
from database import get_session, User
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return "API"

@app.route('/auth/register', methods=['POST'])
def auth_register():
    session = get_session()
    data = request.get_json()
    return jsonify(data)

@app.route('/users', methods=['GET'])
def get_users():
    session = get_session()
    users = session.query(User).all()
    session.close()

    users_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(users_list)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')

    if name:
        session = get_session()
        new_user = User(name=name)
        session.add(new_user)
        session.commit()
        session.close()
        return jsonify({"message": f"Utilisateur '{name}' ajouté."}), 201
    return jsonify({"error": "Nom de l'utilisateur manquant."}), 400

def run_flask(host, port, shutdown_event):
    server_thread = threading.Thread(target=lambda: app.run(host=host, port=port))
    server_thread.start()
    while not shutdown_event.is_set():
        pass
    server_thread.join()
