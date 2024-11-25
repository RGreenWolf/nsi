import requests
import time
import json
import os
import sys

# baseURL = "http://localhost:5000"
baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"

token_file = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else 'client.json'
username = None
token = None
party = {}

# Fonction pour charger le token depuis le fichier
def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            data = json.load(file)
            return data.get('token')
    return None

# Fonction pour sauvegarder le token dans le fichier
def save_token(token):
    with open(token_file, 'w') as file:
        json.dump({'token': token}, file)

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
        save_token(token)
        return token
    else:
        print(f"Erreur lors de la connexion : {res.json().get('message')}")
        return login()

# Fonction pour consulter le classement
def view_rankings(token):
    res = requests.get(baseURL + "/rankings", params={"token": token})
    rankings = res.json().get("rankings", [])
    if not rankings:
        print("Aucun classement disponible pour le moment.")
        return
    print("Classement des joueurs :")
    for rank, player in enumerate(rankings, 1):
        print(f"{rank}. {player['username']} - {player['wins']} victoires")

# Fonction pour démarrer une partie
def startGame(token, username, party):
    status = "pending"
    last_message = ""

    while status != "end":
        res = requests.get(baseURL + "/party/status", params={"token": token})
        party_data = res.json()
        status = party_data.get("status")

        if party_data.get("status") == "error":
            print(f"Erreur : {party_data.get('message')}")
            break

        current_message = ""

        if status == "pending":
            current_message = "En attente d'un autre joueur..."

        elif status == "start":
            my_turn = party_data.get("my_turn")
            current_player = party_data.get("current_player")
            if my_turn:
                num = int(input("Entrez un nombre : "))
                res = requests.post(baseURL + "/party/test", json={"token": token, "num": num})
                result = res.json()
                status = result.get("status")
                current_message = result.get("message")
            else:
                current_message = f"C'est au tour de {current_player} de jouer."

        if current_message and current_message != last_message:
            print(current_message)
            last_message = current_message

        time.sleep(0.5)

    endGame = requests.get(baseURL + "/party/status", params={"token": token}).json()
    if endGame.get("status") == "end":
        print("Fin de la partie le gagnant est :", endGame.get("winner"))

# Vérification du token
def verifyToken(token):
    verify = requests.get(baseURL + "/auth/check_token", params={"token": token})
    verify = verify.json()
    if verify['status'] == 'success':
        return verify['username']
    else:
        os.remove(token_file)
        return None

# Fonction principale
def main():
    token = load_token() if os.path.exists(token_file) else None
    if token:
        username = verifyToken(token)
    else:
        choice = input("Voulez-vous vous inscrire (r) ou vous connecter (l) ? ").lower()
        if choice == "r":
            token = register()
        elif choice == "l":
            token = login()
        username = verifyToken(token)

    if not token or not username:
        print("Veuillez relancer le jeu.")
        exit()

    while True:

        # Menu principal après connexion
        menu = input("\nRejoindre ou créer une partie ou trouver une partie (j/c/r)\nConsulter le classement (v)\nQuitter (exit)\n").lower()
        try:
            if menu == "j":
                party_id = input("Entrez l'identifiant de la partie : ")
                res = requests.post(baseURL + "/party/join", json={"id": party_id, "token": token})
                if res.json().get("status") == "error":
                    print(f"Erreur : {res.json().get('message')}")
                    continue
                else:
                    party["id"] = party_id
                    print(f"Vous avez rejoint la partie {party_id}, le nombre est compris entre 1 et {res.json().get('difficulty')}")
                    startGame(token, username, party)

            elif menu == "c":
                difficulty = int(input("Entrez la difficulté (un nombre entier) : "))
                public = input("Voulez-vous que la partie soit publique (o/n) ? ").lower()
                res = requests.post(baseURL + "/party/create", json={"difficulty": difficulty, "token": token, "public": public == "o"})
                if res.json().get("status") == "error":
                    print(f"Erreur : {res.json().get('message')}")
                    continue
                else:
                    party["id"] = res.json().get("id")
                    print(f"Partie créée avec l'ID : {party['id']}")
                    startGame(token, username, party)

            elif menu == "t":
                res = requests.get(baseURL + "/party/random", params={"token": token})
                if res.json().get("status") == "error":
                    print(f"Erreur : {res.json().get('message')}")
                    continue
                else:
                    party["id"] = res.json().get("id")
                    print(f"Vous avez rejoint la partie {party['id']}, le nombre est compris entre 1 et {res.json().get('difficulty')}")
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
