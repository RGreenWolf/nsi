import threading
from flask import Flask, request, jsonify
import uuid
import random
import json
import os
import time
import hashlib

app = Flask(__name__)

stop = False
tps = 0

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
    def __init__(self, player, difficulty, public=False):
        self.id = str(uuid.uuid4()).split("-")[0]
        self.players = [player]
        self.max_players = 2
        self.difficulty = int(difficulty)
        self.status = "pending"
        self.public = public
        self.num = random.randint(1, self.difficulty)
        self.current_player = player
        self.winner = None
        self.playerData = {}
        self.playerData[player] = {
            "time": getTimeArrond(),
            "attempts": 0
        }
        self.time = {
            "start": getTimeArrond(),
            "end": None
        }
        print(f"Création de la partie {self.id} avec le nombre {self.num}")

    def addPlayer(self, player):
        if player in self.players:
            return False
        self.players.append(player)
        self.playerData[player] = {
            "time": getTimeArrond(),
            "attempts": 0
        }
        self.start()
        return True

    def start(self):
        if len(self.players) == self.max_players:
            self.current_player = random.choice(self.players)
            self.status = "start"

    def isPlayerInGame(self, player):
        return player in self.players
    
    def isPlayerTurn(self, player):
        return self.current_player == player

    def switch_turn(self):
        if len(self.players) == 2:
            self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
    
    def getPointsWin(self, player):
        print(self.playerData[player]["attempts"])
        return round(self.difficulty/self.playerData[player]["attempts"] * 10, 2)

    def win(self, player):
        self.winner = player
        self.time["end"] = getTimeArrond()
        self.status = "end"
        users[player]["wins"] += 1
        users[player]["points"] += self.getPointsWin(player)
        save_data('users.json', users)

    def forfait(self, player):
        self.players.remove(player)
        if self.players:
            self.win(self.players[0])
        else:
            self.status = "end"
        save_data('users.json', users)

    def addAttempt(self, player):
        if player in self.playerData:
            if "attempts" not in self.playerData[player]:
                self.playerData[player]["attempts"] = 0
            self.playerData[player]["attempts"] += 1

    def checkMaxPlayers(self):
        return len(self.players) == self.max_players

    def getWinner(self):
        return self.winner

    def getStatus(self, player):
        return {
            "id": self.id,
            "players": self.players,
            "difficulty": self.difficulty,
            "status": self.status,
            "current_player": self.current_player,
            "my_turn": self.isPlayerTurn(player),
            "winner": self.winner
        }

def getTimeArrond():
    return round(time.time())

# Fonction de hachage du mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction utilitaire pour obtenir le nom d'utilisateur à partir d'un token
def getUsername(token):
    if token in tokens: 
        return tokens[token]
    else:
        print("sa")

# Vérifier si un joueur est déjà dans une partie active
def isPlayerInGameKick(player):
    for party in parties.values():
        if player in party.players and party.status != "end":
            party.players.remove(player)
            if party.players:  # Check if there are still players left
                playerTemp = party.players[0]
                users[playerTemp]["wins"] += 1
            party.status = "end"

def getParty(player):
    for party in parties.values():
        if player in party.players:
            return party
    return None

def isPartyExiste(party_id):
    return party_id in parties

def getPublicParties():
    return [party for party in parties.values() if party.public and party.status == "pending" and not party.checkMaxPlayers()]

# Route pour l'inscription d'un utilisateur
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password or len(username) < 3 or len(password) < 6 or len(username) > 20 or len(password) > 30:
        return jsonify({"status": "error", "message": "Données invalides"}), 400
    
    if username in users:
        return jsonify({"status": "error", "message": "L'utilisateur existe déjà"}), 400

    users[username] = {"password": hash_password(password), "wins": 0, "points": 0, }
    save_data('users.json', users)
    return jsonify({"status": "success", "message": "Utilisateur enregistré avec succès"})


# Route pour la connexion d'un utilisateur
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password or len(username) < 3 or len(password) < 6 or len(username) > 20 or len(password) > 30:
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
    
    if tokens.get(token):
        return jsonify({"status": "success", "message": "Token valide", "username": tokens[token]})
    else:
        return jsonify({"status": "error", "message": "Token invalide"}), 403

# Route pour créer une partie
@app.route('/party/create', methods=['POST'])
def party_create():
    data = request.json
    token = data.get("token")
    difficulty = int(data.get("difficulty"))
    public = int(data.get("public")) if data.get("public") else False

    player = getUsername(token)
    if not player or not difficulty or player not in users or difficulty < 0:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    isPlayerInGameKick(player)

    new_party = Party(player, difficulty, public)
    new_party.playerData[player]
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

    if isPartyExiste(party_id):
        party = parties[party_id]
        if len(party.players) >= party.max_players:
            party.start()
            return jsonify({"status": "error", "message": "La partie est déjà pleine"}), 400
        
        if not party.addPlayer(player):
            return jsonify({"status": "error", "message": "Le pseudo est déjà pris"}), 400

        return jsonify({"status": party.status, "difficulty": party.difficulty})
    else:
        return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour obtenir le statut d'une partie
@app.route('/party/status', methods=['GET'])
def party_status():
    token = request.args.get("token")
    username = getUsername(token)
    party = getParty(username)

    if party:
        party.playerData[username]["time"] = getTimeArrond()
        return jsonify(party.getStatus(username))
    else:
        return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour tester un nombre dans le jeu
@app.route('/party/test', methods=['POST'])
def party_test():
    data = request.json

    token = data.get("token")
    num = data.get("num")

    username = getUsername(token)
    party = getParty(username)

    if not party or not username or num is None:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    party.addAttempt(username)
    if party:
        if not party.isPlayerTurn(username):
            return jsonify({"status": party.status, "message": "Ce n'est pas votre tour"}), 403
        if party.num == num:
            party.win(username)
            return jsonify({"status": party.status, "message": "Bravo ! Vous avez trouvé le nombre."})
        elif party.num < num:
            party.switch_turn()
            return jsonify({"status": party.status, "message": "Trop grand"})
        elif party.num > num:
            party.switch_turn()
            return jsonify({"status": party.status, "message": "Trop petit"})
    else:
        return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

@app.route('/party/random', methods=['GET'])
def party_random():
    token = request.args.get("token")
    username = getUsername(token)
    if not username:
        return jsonify({"status": "error", "message": "Token invalide"}), 400

    parties_public = getPublicParties()

    if len(parties_public) == 0:
        return jsonify({"status": "error", "message": "Aucune partie publique disponible"}), 404

    party_id = random.choice([party.id for party in parties_public])
    if isPartyExiste(party_id):
        party = parties[party_id]
        return jsonify({"status": party.status, "id": party.id, "difficulty": party.difficulty})
    

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
        "rankings": [
            {"username": user[0], "wins": user[1]["wins"]} for user in top_20],
        "your_rank": player_rank
    })

@app.route('/parties/public', methods=['GET'])
def get_public_parties():
    return jsonify({
        "parties": [
            {"id": party.id, "difficulty": party.difficulty} for party in getPublicParties()
        ]
    })

def commande():
    global stop
    global tps
    while True :
        cmd = input("")
        if cmd == "exit":
            stop = True
        elif cmd == "tps":
            print(f"Temps d'exécution moyen : {tps} secondes")
        elif cmd == "users":
            for user in users:
                print(f"{user} : {users[user].get('wins')} victoires")
        elif cmd == "tokens":
            for token in tokens:
                print(f"{token} : {tokens[token]}")
        elif cmd == "parties":
            for party in parties.values():
                print(f"{party.id} : {party.players} - {party.status}")
        elif cmd == "save":
            save_data('users.json', users)
            save_data('tokens.json', tokens)
            print("Données sauvegardées")
        else:
            print("Commande inconnue")
        print("\n")

def ticks():
    tick_count = 0
    timeToTick = time.time()
    global stop
    global tps
    while True:
        timeToTick = time.time()
        if tick_count % 10 == 0 and tick_count != 0:
            for party in list(parties.values()):
                if party.status == "end" and len(party.players) < 2:
                    del parties[party.id]

        if tick_count % 120 == 0 and tick_count != 0:
            save_data('users.json', users)
            save_data('tokens.json', tokens)
            print("Données sauvegardées")

        for party in list(parties.values()):
            if party.status == "start" and party.checkMaxPlayers() and getTimeArrond() - party.playerData[party.current_player]["time"] > 60 :
                for player in list(party.players):
                    if getTimeArrond() - party.playerData[player]["time"] > 60:
                        party.forfait(player)
                        print(f"Le joueur {player} a été exclu de la partie {party.id} pour inactivité")
    
        if stop:
            break
        
        tps = time.time() - timeToTick + 1
        time.sleep(1)
        tick_count += 1
    os._exit(0)

def startServer():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

threadCmd = threading.Thread(target=commande)
threadWeb = threading.Thread(target=startServer)
threadTicks = threading.Thread(target=ticks)

def init(): 
    for user in users:
        if "wins" not in users[user]:
            users[user]["wins"] = 0
        if "points" not in users[user]:
            users[user]["points"] = 0
    save_data('users.json', users)

if __name__ == '__main__':
    try:
        init()
        threadWeb.start()
        threadTicks.start()
        threadCmd.start()
        threadCmd.join() 
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        stop = True
        threadWeb.join()
        threadTicks.join()
