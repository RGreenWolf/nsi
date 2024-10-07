from flask import Flask, request, jsonify
import uuid
import random
import json
import os
import hashlib

app = Flask(__name__)

# Charger ou initialiser les utilisateurs et les classements depuis les fichiers JSON
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

users = load_data('users.json')
tokens = load_data('tokens.json')
parties = {}

# Classe de partie
class Party:
    def __init__(self, player, difficulty):
        self.id = str(uuid.uuid4()).split("-")[0]
        self.players = [player]
        self.difficulty = int(difficulty)
        self.status = "pending"
        self.num = random.randint(1, self.difficulty)
        self.current_player = player
        print(f"Création de la partie {self.id} avec le nombre {self.num}")

    def add_player(self, player):
        if player in self.players:
            return False
        self.players.append(player)
        if len(self.players) == 2:
            self.status = "start"
        return True

    def switch_turn(self):
        if len(self.players) == 2:
            self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

# Fonction de hachage du mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction utilitaire pour obtenir le nom d'utilisateur à partir d'un token
def getUsername(token):
    return tokens[token]

# Vérifier si un joueur est déjà dans une partie active
def isPlayerInGameKick(player):
    for party in parties.values():
        if player in party.players and party.status != "end":            
            party.status = "end"

# Route pour l'inscription d'un utilisateur
@app.route('/auth/register', methods=['POST'])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Données invalides"}), 400
    
    if username in users:
        return jsonify({"status": "error", "message": "L'utilisateur existe déjà"}), 400

    users[username] = {"password": hash_password(password), "wins": 0}
    save_data('users.json', users)
    return jsonify({"status": "success", "message": "Utilisateur enregistré avec succès"})


# Route pour la connexion d'un utilisateur
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Données invalides"}), 400
    
    user = users.get(username)
    if not user or user["password"] != hash_password(password):
        return jsonify({"status": "error", "message": "Identifiant ou mot de passe incorrect"}), 403

    token = str(uuid.uuid4())
    tokens[token] = username
    save_data('tokens.json', tokens)
    return jsonify({"status": "success", "message": "Connexion réussie", "token": token})

@app.route('/auth/check_token', methods=['GET'])
def check_token():
    token = request.args.get("token")
    if not token:
        return jsonify({"status": "error", "message": "Token manquant"}), 400
    
    if token in tokens:
        return jsonify({"status": "success", "message": "Token valide"})
    else:
        return jsonify({"status": "error", "message": "Token invalide"}), 403

# Route pour créer une partie
@app.route('/party/create', methods=['POST'])
def party_create():
    data = request.json
    token = data.get("token")
    difficulty = data.get("difficulty")

    player = getUsername(token)
    if not player or not difficulty or player not in users:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    isPlayerInGameKick(player)

    new_party = Party(player, difficulty)
    parties[new_party.id] = new_party
    return jsonify({"status": "success", "id": new_party.id})


# Route pour rejoindre une partie
@app.route('/party/join', methods=['POST'])
def party_join():
    data = request.json
    party_id = data.get("id")
    token = data.get("token")

    player = getUsername(token)
    if not party_id or not player or player not in users:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    isPlayerInGameKick(player)

    if parties[party_id]:
        party = parties[party_id]
        if len(party.players) >= 2:
            return jsonify({"status": "error", "message": "La partie est déjà pleine"}), 400
        
        if not party.add_player(player):
            return jsonify({"status": "error", "message": "Le pseudo est déjà pris"}), 400
        
        return jsonify({"status": party.status})
    else:
        return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour obtenir le statut d'une partie
@app.route('/party/status', methods=['GET'])
def party_status():
    party_id = request.args.get("id")

    if not party_id:
        return jsonify({"status": "error", "message": "ID de la partie manquant"}), 400

    if parties[party_id]:
        party = parties[party_id]
        return jsonify({
            "id": party.id,
            "players": party.players,
            "difficulty": party.difficulty,
            "status": party.status,
            "current_player": party.current_player
        })
    else:
        return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour tester un nombre dans le jeu
@app.route('/party/test', methods=['POST'])
def party_test():
    data = request.json
    party_id = data.get("id")
    token = data.get("token")
    num = data.get("num")

    player = getUsername(token)
    if not party_id or not player or num is None:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    if parties[party_id]:
        party = parties[party_id]
        if party.current_player != player:
            return jsonify({"status": "error", "message": "Ce n'est pas votre tour"}), 403
        if party.num == num:
            party.status = "end"
            parties.remove(party)
            users[player]["wins"] += 1
            save_data('users.json', users)
            return jsonify({"status": "end", "message": "Bravo ! Vous avez trouvé le nombre."})
        elif party.num < num:
            party.switch_turn()
            return jsonify({"status": "start", "message": "Trop grand"})
        elif party.num > num:
            party.switch_turn()
            return jsonify({"status": "start", "message": "Trop petit"})
    else:
        return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour obtenir le classement
@app.route('/rankings', methods=['GET'])
def get_rankings():
    token = request.args.get("token")
    player = getUsername(token)

    if not player:
        return jsonify({"status": "error", "message": "Token invalide"}), 400

    sorted_users = sorted(users.items(), key=lambda x: x[1]["wins"], reverse=True)
    top_20 = sorted_users[:20]
    player_rank = next((i+1 for i, user in enumerate(sorted_users) if user[0] == player), None)

    return jsonify({
        "rankings": [{user[0]: user[1]["wins"]} for user in top_20],
        "your_rank": player_rank
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
