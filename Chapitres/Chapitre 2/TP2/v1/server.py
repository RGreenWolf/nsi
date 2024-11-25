from flask import Flask, request, jsonify
import uuid
import random

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

parties = []

app = Flask(__name__)

# Route pour créer une partie
@app.route('/party/create', methods=['POST'])
def party_create():
    data = request.json
    player = data.get("player")
    difficulty = data.get("difficulty")
    
    if not player or not difficulty:
        return jsonify({"status": "error", "message": "Données invalides"}), 400
    
    new_party = Party(player, difficulty)
    parties.append(new_party)
    return jsonify({"status": "success", "id": new_party.id})

# Route pour rejoindre une partie
@app.route('/party/join', methods=['POST'])
def party_join():
    data = request.json
    party_id = data.get("id")
    player = data.get("player")

    if not party_id or not player:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    for party in parties:
        if party.id == party_id:
            if len(party.players) >= 2:
                return jsonify({"status": "error", "message": "La partie est déjà pleine"}), 400
            
            if not party.add_player(player):
                return jsonify({"status": "error", "message": "Le pseudo est déjà pris"}), 400
            
            return jsonify({"status": party.status})
    
    return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour obtenir le statut d'une partie
@app.route('/party/status', methods=['GET'])
def party_status():
    party_id = request.args.get("id")

    if not party_id:
        return jsonify({"status": "error", "message": "ID de la partie manquant"}), 400

    for party in parties:
        if party.id == party_id:
            return jsonify({
                "id": party.id,
                "players": party.players,
                "difficulty": party.difficulty,
                "status": party.status,
                "current_player": party.current_player
            })
    
    return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

# Route pour tester un nombre dans le jeu
@app.route('/party/test', methods=['POST'])
def party_test():
    data = request.json
    party_id = data.get("id")
    player = data.get("player")
    num = data.get("num")

    if not party_id or not player or num is None:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    for party in parties:
        if party.id == party_id:
            if party.current_player != player:
                return jsonify({"status": "error", "message": "Ce n'est pas votre tour"}), 403
            if party.num == num:
                party.status = "end"
                parties.remove(party)
                return jsonify({"status": "end", "message": "Bravo ! Vous avez trouvé le nombre."})
            elif party.num < num:
                party.switch_turn()
                return jsonify({"status": "start", "message": "Trop grand"})
            elif party.num > num:
                party.switch_turn()
                return jsonify({"status": "start", "message": "Trop petit"})
    
    return jsonify({"status": "error", "message": "Partie non trouvée"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25000, debug=False)
