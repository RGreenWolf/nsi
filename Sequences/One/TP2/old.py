import requests
import time
 
# baseURL = "http://localhost:5000"
 
baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"
 
player = input("Entrez votre nom : ")
 
mode = input("Rejoindre ou créer une partie (r/c) : ")
 
party = {}
 
if mode.lower() == "r":
    party_id = input("Entrez l'identifiant de la partie : ")
    res = requests.post(baseURL + "/party/join", json={"id": party_id, "player": player})
    if res.json().get("status") == "error":
        print(f"Erreur : {res.json().get('message')}")
        exit()
    else:
        party["id"] = party_id
        print(f"Vous avez rejoint la partie {party_id}")
 
if mode.lower() == "c":
    difficulty = int(input("Entrez la difficulté (un nombre entier) : "))
    res = requests.post(baseURL + "/party/create", json={"player": player, "difficulty": difficulty})
    party["id"] = res.json().get("id")
    print(f"Partie créée avec l'ID : {party['id']}")
 
status = "pending"
last_message = ""
 
while status != "end":
    res = requests.get(baseURL + "/party/status", params={"id": party.get("id")})
    party = res.json()
    status = party.get("status")
    if party.get("status") == "error":
        print(f"Erreur : {party.get('message')}")
        break
 
    current_message = ""
    if party.get("status") == "pending":
        current_message = f"En attente d'un autre joueur... (ID de la partie : {party.get('id')})"
   
    elif party.get("status") == "start":
        current_player = party.get("current_player")
        if current_player == player:
            num = int(input("Entrez un nombre : "))
            res = requests.post(baseURL + "/party/test", json={"id": party.get("id"), "player": player, "num": num})
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