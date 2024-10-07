import requests
import time
import json
import os

baseURL = "http://localhost:5000"
# baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"

# Fichier pour stocker le token
token_file = 'client.json'

# Fonction pour charger le token à partir du fichier
def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            return json.load(file).get('token')
    return None

# Fonction pour sauvegarder le token dans le fichier
def save_token(token):
    with open(token_file, 'w') as file:
        json.dump({'token': token}, file)

# Fonction pour l'inscription
def register():
    username = input("Choisissez un nom d'utilisateur : ")
    password = input("Choisissez un mot de passe : ")
    res = requests.post(baseURL + "/user/register", json={"username": username, "password": password})
    if res.json().get("status") == "success":
        print("Inscription réussie !")
        return login()  # Connexion immédiate après inscription
    else:
        print(f"Erreur lors de l'inscription : {res.json().get('message')}")
        exit()

# Fonction pour la connexion
def login():
    username = input("Entrez votre nom d'utilisateur : ")
    password = input("Entrez votre mot de passe : ")
    res = requests.post(baseURL + "/user/login", json={"username": username, "password": password})
    if res.json().get("status") == "success":
        print("Connexion réussie !")
        token = res.json().get("token")
        save_token(token)  # Enregistrer le token dans le fichier
        return token
    else:
        print(f"Erreur lors de la connexion : {res.json().get('message')}")
        exit()

# Fonction pour consulter le classement
def view_rankings(token):
    res = requests.get(baseURL + "/rankings", params={"token": token})
    rankings = res.json().get("rankings", [])
    your_rank = next((rank + 1 for rank, player in enumerate(rankings) if player.get(username) is not None), None)
    
    if rankings:
        print("Classement des joueurs :")
        for rank, player in enumerate(rankings, 1):
            for name, wins in player.items():
                print(f"{rank}. {name} - {wins} victoires")
    else:
        print("Aucun classement disponible pour le moment.")
    
    if your_rank:
        print(f"Votre position : {your_rank}")

# Menu principal : Inscription, Connexion ou Classement
username = None
token = load_token()

if token:
    print("Token chargé avec succès.")
else:
    choice = input("Voulez-vous vous inscrire (r) ou vous connecter (l) ? ").lower()
    if choice == "r":
        token = register()
    elif choice == "l":
        token = login()
    else:
        print("Choix invalide.")
        exit()

# Choisir de créer ou rejoindre une partie
mode = input("Rejoindre ou créer une partie (r/c) : ").lower()

party = {}

if mode == "r":
    party_id = input("Entrez l'identifiant de la partie : ")
    res = requests.post(baseURL + "/party/join", json={"id": party_id, "token": token})
    if res.json().get("status") == "error":
        print(f"Erreur : {res.json().get('message')}")
        exit()
    else:
        party["id"] = party_id
        print(f"Vous avez rejoint la partie {party_id}")

elif mode == "c":
    difficulty = int(input("Entrez la difficulté (un nombre entier) : "))
    res = requests.post(baseURL + "/party/create", json={"difficulty": difficulty, "token": token})
    if res.json().get("status") == "error":
        print(f"Erreur : {res.json().get('message')}")
        exit()
    else:
        party["id"] = res.json().get("id")
        print(f"Partie créée avec l'ID : {party['id']}")

else:
    print("Choix invalide.")
    exit()

# Boucle principale de jeu
status = "pending"
last_message = ""

while status != "end":
    res = requests.get(baseURL + "/party/status", params={"id": party.get("id")})
    party_data = res.json()
    status = party_data.get("status")

    if party_data.get("status") == "error":
        print(f"Erreur : {party_data.get('message')}")
        break

    current_message = ""

    if party_data.get("status") == "pending":
        current_message = "En attente d'un autre joueur..."

    elif party_data.get("status") == "start":
        current_player = party_data.get("current_player")
        if current_player == res.json().get("current_player"):  # Vérifie si c'est à votre tour
            num = int(input("Entrez un nombre : "))
            res = requests.post(baseURL + "/party/test", json={"id": party.get("id"), "token": token, "num": num})
            result = res.json()
            status = result.get("status")
            current_message = result.get("message")
        else:
            current_message = f"C'est au tour de {current_player} de jouer."

    if current_message and current_message != last_message:
        print(current_message)
        last_message = current_message

    time.sleep(1)

if status == "end":
    print("Fin de la partie")
