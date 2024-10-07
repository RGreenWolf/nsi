import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
import sys
import time
import threading

baseURL = "http://localhost:5000"
token_file = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else 'client.json'

def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            data = json.load(file)
            return data
    return None

def save_token(token, username):
    with open(token_file, 'w') as file:
        json.dump({'token': token, 'username': username}, file)

def auto_login():
    save = load_token()
    if save:
        token = save.get('token')
        username = save.get('username')
        if token:
            res = requests.get(baseURL + "/auth/check_token", params={"token": token})
            if res.json().get("status") == "success":
                messagebox.showinfo("Connexion réussie", f"Re-bienvenue {username} !")
                main_menu_frame.tkraise()
                return True
            else:
                messagebox.showerror("Erreur", "Le token a expiré. Veuillez vous reconnecter.")
                return False
    return False

def register():
    username = username_entry.get()
    password = password_entry.get()
    res = requests.post(baseURL + "/auth/register", json={"username": username, "password": password})
    if res.json().get("status") == "success":
        messagebox.showinfo("Inscription réussie", "Vous pouvez maintenant vous connecter.")
        login_frame.tkraise()
    else:
        messagebox.showerror("Erreur", res.json().get("message"))

def login():
    username = username_entry.get()
    password = password_entry.get()
    res = requests.post(baseURL + "/auth/login", json={"username": username, "password": password})
    if res.json().get("status") == "success":
        token = res.json().get("token")
        save_token(token, username)
        messagebox.showinfo("Connexion réussie", "Bienvenue !")
        main_menu_frame.tkraise()
    else:
        messagebox.showerror("Erreur", res.json().get("message"))

def create_game():
    token = load_token().get("token")
    difficulty = int(difficulty_entry.get())
    res = requests.post(baseURL + "/party/create", json={"difficulty": difficulty, "token": token})
    if res.json().get("status") == "success":
        party_id = res.json().get("id")
        messagebox.showinfo("Partie créée", f"Partie créée avec l'ID : {party_id}")
        party_id_entry.delete(0, tk.END)
        party_id_entry.insert(0, party_id)
        game_frame.tkraise()
        start_game(party_id)
    else:
        messagebox.showerror("Erreur", res.json().get("message"))

def join_game():
    party_id = party_id_entry.get()
    token = load_token().get("token")
    res = requests.post(baseURL + "/party/join", json={"id": party_id, "token": token})
    if res.json().get("status") == "error":
        messagebox.showerror("Erreur", res.json().get("message"))
    else:
        messagebox.showinfo("Succès", f"Vous avez rejoint la partie {party_id}")
        game_frame.tkraise()
        start_game(party_id)

def start_game(party_id):
    def game_loop():
        token = load_token().get("token")
        username = load_token().get("username")
        status = "pending"
        last_message = ""

        while status != "end":
            res = requests.get(baseURL + "/party/status", params={"id": party_id})
            party_data = res.json()
            status = party_data.get("status")

            if party_data.get("status") == "error":
                messagebox.showerror("Erreur", party_data.get("message"))
                break

            current_message = ""

            if status == "pending":
                current_message = "En attente d'un autre joueur..."

            elif status == "start":
                current_player = party_data.get("current_player")
                if current_player == username:
                    current_message = "C'est votre tour ! Entrez un nombre."
                else:
                    current_message = f"C'est au tour de {current_player} de jouer."

            if current_message != last_message:
                game_message_label.config(text=current_message)
                last_message = current_message

            if status == "start" and party_data.get("current_player") == username:
                try:
                    num = int(number_entry.get())
                    res = requests.post(baseURL + "/party/test", json={"id": party_id, "token": token, "num": num})
                    result = res.json()
                    status = result.get("status")
                    game_message_label.config(text=result.get("message"))

                    # Affichage spécial pour "Trop grand" ou "Trop petit"
                    if "Trop grand" in result.get("message"):
                        game_hint_label.config(text="Le nombre est trop grand !", fg="red")
                    elif "Trop petit" in result.get("message"):
                        game_hint_label.config(text="Le nombre est trop petit !", fg="blue")
                    else:
                        game_hint_label.config(text="")
                except ValueError:
                    messagebox.showwarning("Erreur", "Veuillez entrer un nombre valide.")
                    continue

            time.sleep(1)

        if status == "end":
            game_message_label.config(text="Fin de la partie")
    
    threading.Thread(target=game_loop).start()

def copy_party_id():
    party_id = party_id_entry.get()
    root.clipboard_clear()
    root.clipboard_append(party_id)
    messagebox.showinfo("ID copié", f"L'ID de la partie {party_id} a été copié dans le presse-papiers.")

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Jeu de Devine Nombre")

login_frame = tk.Frame(root)
register_frame = tk.Frame(root)
main_menu_frame = tk.Frame(root)
game_frame = tk.Frame(root)

for frame in (login_frame, register_frame, main_menu_frame, game_frame):
    frame.grid(row=0, column=0, sticky='news')

# Écran de connexion
tk.Label(login_frame, text="Connexion").grid(row=0, column=1)
tk.Label(login_frame, text="Nom d'utilisateur").grid(row=1, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=1, column=1)
tk.Label(login_frame, text="Mot de passe").grid(row=2, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=2, column=1)
tk.Button(login_frame, text="Connexion", command=login).grid(row=3, column=1)
tk.Button(login_frame, text="Inscription", command=lambda: register_frame.tkraise()).grid(row=4, column=1)

# Écran d'inscription
tk.Label(register_frame, text="Inscription").grid(row=0, column=1)
tk.Label(register_frame, text="Nom d'utilisateur").grid(row=1, column=0)
username_entry = tk.Entry(register_frame)
username_entry.grid(row=1, column=1)
tk.Label(register_frame, text="Mot de passe").grid(row=2, column=0)
password_entry = tk.Entry(register_frame, show="*")
password_entry.grid(row=2, column=1)
tk.Button(register_frame, text="S'inscrire", command=register).grid(row=3, column=1)
tk.Button(register_frame, text="Retour à la connexion", command=lambda: login_frame.tkraise()).grid(row=4, column=1)

# Écran du menu principal
tk.Label(main_menu_frame, text="Menu Principal").grid(row=0, column=1)
party_id_entry = tk.Entry(main_menu_frame)
party_id_entry.grid(row=1, column=1)
tk.Label(main_menu_frame, text="ID de la partie").grid(row=1, column=0)
tk.Button(main_menu_frame, text="Rejoindre Partie", command=join_game).grid(row=2, column=1)

difficulty_entry = tk.Entry(main_menu_frame)
difficulty_entry.grid(row=3, column=1)
tk.Label(main_menu_frame, text="Difficulté").grid(row=3, column=0)
tk.Button(main_menu_frame, text="Créer Partie", command=create_game).grid(row=4, column=1)

# Bouton pour copier l'ID de la partie
tk.Button(main_menu_frame, text="Copier l'ID de la Partie", command=copy_party_id).grid(row=5, column=1)

# Écran de jeu
tk.Label(game_frame, text="Jeu en cours").grid(row=0, column=1)
game_message_label = tk.Label(game_frame, text="En attente...")
game_message_label.grid(row=1, column=1)
number_entry = tk.Entry(game_frame)
number_entry.grid(row=2, column=1)
tk.Label(game_frame, text="Entrez un nombre").grid(row=2, column=0)
game_hint_label = tk.Label(game_frame, text="")
game_hint_label.grid(row=3, column=1)
tk.Button(game_frame, text="Envoyer", command=lambda: start_game(party_id_entry.get())).grid(row=4, column=1)
tk.Button(game_frame, text="Quitter", command=lambda: main_menu_frame.tkraise()).grid(row=5, column=1)

if not auto_login():
    login_frame.tkraise()

root.mainloop()
