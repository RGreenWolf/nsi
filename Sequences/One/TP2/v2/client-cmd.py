import requests
import time
import json
import os
import sys

baseURL = "http://localhost:5000"  # URL du serveur
# baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"  # Pour un usage distant

token_file = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else 'client.json'  # Fichier de sauvegarde du token local
username = None  # Variable pour stocker le nom d'utilisateur localement

# Fonction pour charger le token depuis le fichier
def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            data = json.load(file)
            return data
    return None

# Fonction pour sauvegarder le token dans le fichier
def save_token(token, username):
    with open(token_file, 'w') as file:
        json.dump({'token': token, 'username': username}, file)

# Fonction d'inscription
def register():
    username = input("Choisissez un nom d'utilisateur : ")
    password = input("Choisissez un mot de passe : ")
    res = requests.post(baseURL + "/auth/register", json={"username": username, "password": password})
    if res.json().get("status") == "success":
        print("Inscription réussie !\nVous pouvez maintenant vous connecter.")
        return login()
    else:
        print(f"Erreur lors de l'inscription : {res.json().get('message')}")
        return None

# Fonction de connexion
def login():
    username = input("Entrez votre nom d'utilisateur : ")
    password = input("Entrez votre mot de passe : ")
    res = requests.post(baseURL + "/auth/login", json={"username": username, "password": password})
    if res.json().get("status") == "success":
        print("Connexion réussie !")
        token = res.json().get("token")
        save_token(token, username)  # Enregistrer le token dans le fichier
        return token
    else:
        print(f"Erreur lors de la connexion : {res.json().get('message')}")
        return None

# Fonction pour consulter le classement
def view_rankings(token):
    res = requests.get(baseURL + "/rankings", params={"token": token})
    rankings = res.json().get("rankings", [])
    if not rankings:
        print("Aucun classement disponible pour le moment.")
        return
    print("Classement des joueurs :")
    for rank, player in enumerate(rankings, 1):
        for name, wins in player.items():
            print(f"{rank}. {name} - {wins} victoires")

# Fonction pour démarrer une partie
def startGame(token, username, party):
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

        if status == "pending":
            current_message = "En attente d'un autre joueur..."

        elif status == "start":
            current_player = party_data.get("current_player")
            if current_player == username:
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

# Fonction principale
def main():
    save = load_token()  # Charger le token sauvegardé
    token = save.get('token') if save else None
    username = save.get('username') if save else None
    party = {}

    while True:
        if not token:  # Si aucun token, proposer inscription ou connexion
            choice = input("Voulez-vous vous inscrire (r) ou vous connecter (l) ? ").lower()
            if choice == "r":
                token = register()
            elif choice == "l":
                token = login()
            elif choice == "exit":
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")
                continue

        if not token:
            exit()

        # Menu principal après connexion
        menu = input("\nRejoindre ou créer une partie (r/c)\nConsulter le classement (v)\nQuitter (exit)\n").lower()
        try:
            if menu == "r":
                party_id = input("Entrez l'identifiant de la partie : ")
                res = requests.post(baseURL + "/party/join", json={"id": party_id, "token": token})
                if res.json().get("status") == "error":
                    print(f"Erreur : {res.json().get('message')}")
                    continue
                else:
                    party["id"] = party_id
                    print(f"Vous avez rejoint la partie {party_id}")
                    startGame(token, username, party)

            elif menu == "c":
                difficulty = int(input("Entrez la difficulté (un nombre entier) : "))
                res = requests.post(baseURL + "/party/create", json={"difficulty": difficulty, "token": token})
                if res.json().get("status") == "error":
                    print(f"Erreur : {res.json().get('message')}")
                    continue
                else:
                    party["id"] = res.json().get("id")
                    print(f"Partie créée avec l'ID : {party['id']}")
                    startGame(token, username, party)

            elif menu == "v":
                view_rankings(token)

            elif menu == "exit":
                print("Au revoir !")
                break

            else:
                print("Choix invalide.")

        except Exception as e:
            print(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    main()