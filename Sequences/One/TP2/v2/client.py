import tkinter as tk
import requests
import sys
import json

baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"
token_file = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else 'client.json'


#pour les Label "dynamyque"
def afficher_label(fenetre, text, relx, rely, font=("Arial", 12), fg="black", bg="#f0f0f0"):
    if relx==None and rely==None :
        label = tk.Label(fenetre, text=text, fg=fg, bg=bg, font=font)
        label.pack()
    else:
        label = tk.Label(fenetre, text=text, fg=fg, bg=bg, font=font)
        label.place(relx=relx, rely=rely, anchor="center")  # Le centre du label est positionné à relx, rely
        return label


# Fonction pour créer une partie
def create_game(fenetre, labels, name):
    name = name.get()
    print("c'est bon")
    res = requests.post(baseURL + "/party/create", json={"player": name, "difficulty": "10"})
    print("tu as envoyé ta requète")
    if res.status_code == 200:
        id = res.json()['id']
        print(f"ID de la partie: {id}")

        new_game_id_label = tk.Label(fenetre, text=f"Nouvelle partie ID: {id}", bg="#f0f0f0", font=("Arial", 12))
        new_game_id_label.place(relx=0.5, rely=0.6 + len(labels)*0.05, anchor="center")  # Centré horizontalement et un peu plus bas

        labels.append(new_game_id_label)
    else:
        print(f"Erreur: {res.status_code}")
    if res.json()['status'] != 'error':
        afficher_label(fenetre,"Tu es connecté", 0.5, 0.9, fg='green')
        fenetre.destroy()
        jeu(id, name)


# Fonction pour rejoindre une partie
def join_party(fenetre, join, name):
    id = join.get()
    name = name.get()
    res = requests.post(baseURL + "/party/join", json={"player": name, "id": id})
    if res.json()['status'] != 'error':
        afficher_label(fenetre,"Tu es connecté", 0.5, 0.9, fg='green')
        fenetre.destroy()
        jeu(id, name)
    else:
        print(f"Erreur: {res.json()['message']} ({res.status_code})")


# Fonction pour envoyer le résultat
def envoyer_result(window, nombre, id, name):
    resultat = nombre.get()
    if resultat.isdigit():
        print(f"le résultat est {resultat}")
        res = requests.post(baseURL + "/party/test", json={"id": id, "player": name, "num": resultat})
        print(res.text)
        player(window)
    else:
        afficher_label(window,"Tu es connecté", None, None, fg='green')

def player(window):
    #envoyer une requête pour avoir current_player
    res={'current_player': 'test'}
    # current_player = res.json()['current_player']
    afficher_label(window, f"a {res['current_player']} de jouer", 0.5, 0.9, font=("Arial", 14))

def requete_connexion(fenetre, entry_login, entry_mdp):
    login = entry_login.get()
    mdp = entry_mdp.get()
    res = requests.post(baseURL + "/auth/login", json={"username": login, "password": mdp})
    if res.json().get("status") == "success":
        print("Connexion réussie !")
        token = res.json().get("token")
        save_token(token)

        connexion(fenetre)
        return token
    else:
        afficher_label(fenetre, f"Erreur : mot de passe ou pseudo invalide",0.5, 0.9)
        print(f"Erreur lors de la connexion : {res.json().get('message')}")
        return None

def requete_register(window, entry_login, entry_mdp):
    login = entry_login.get()
    mdp = entry_mdp.get()
    print(f"login {login} ; mdp {mdp}")

def save_token(token):
    with open(token_file, 'w') as file:
        json.dump({'token': token}, file)

# Interface de jeu
def jeu(id, pseudo):
    window = tk.Tk()
    window.title("Deviner le nombre")
    window.geometry("400x300")  # Taille de la fenêtre

    texte = tk.Label(window, text="Mettez le nombre :", font=("Arial", 14))
    texte.place(relx=0.5, rely=0.3, anchor="center")

    nombre = tk.Entry(window, font=("Arial", 12), bd=2, relief="solid")
    nombre.place(relx=0.5, rely=0.5, anchor="center")

    bouton_validez = tk.Button(window, text="Validez", command=lambda: envoyer_result(window, nombre, id, pseudo),
                               font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
    bouton_validez.place(relx=0.5, rely=0.7, anchor="center")

    player(window)
    window.mainloop()

# Interface du connexion principal
def connexion(windows):
    windows.destroy()
    fenetre = tk.Tk()
    fenetre.title("Deviner le nombre")
    fenetre.geometry("400x500")  # Taille de la fenêtre
    fenetre.configure(bg="#f0f0f0")  # Couleur de fond

    labels = []

    # Label et entrée pour le pseudo
    pseudo_text = tk.Label(fenetre, text="Entrez votre pseudo :", bg="#f0f0f0", font=("Arial", 14))
    pseudo_text.place(relx=0.5, rely=0.1, anchor="center")  # Centré en haut

    pseudo = tk.Entry(fenetre, font=("Arial", 12), bd=2, relief="solid")
    pseudo.place(relx=0.5, rely=0.2, anchor="center")

    # Bouton pour commencer une nouvelle partie
    start = tk.Button(fenetre, text="Commencer la partie", command=lambda: create_game(fenetre, labels, pseudo),
                      font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
    start.place(relx=0.5, rely=0.3, anchor="center")

    # Label et entrée pour rejoindre une partie
    name_label = tk.Label(fenetre, text="Entrez votre pseudo :", bg="#f0f0f0", font=("Arial", 14))
    name_label.place(relx=0.5, rely=0.4, anchor="center")
    name_join = tk.Entry(fenetre, font=("Arial", 12), bd=2, relief="solid")
    name_join.place(relx=0.5, rely=0.5, anchor="center")

    name_label = tk.Label(fenetre, text="Entrez l'ID de la partie :", bg="#f0f0f0", font=("Arial", 14))
    name_label.place(relx=0.5, rely=0.6, anchor="center")
    join = tk.Entry(fenetre, font=("Arial", 12), bd=2, relief="solid")
    join.place(relx=0.5, rely=0.7, anchor="center")

    # Bouton pour rejoindre une partie
    button_join = tk.Button(fenetre, text="Rejoindre", command=lambda: join_party(fenetre, join, name_join),
                            font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=5)
    button_join.place(relx=0.5, rely=0.8, anchor="center")

    fenetre.mainloop()

def création_compte(windows):
    windows.destroy()
    fenetre=tk.Tk()
    fenetre.geometry('300x300')
    Label_login = tk.Label(fenetre, text="entrez votre pseudo  :")
    Label_login.place(relx=0.5, rely=0.1, anchor="center")
    entry_login = tk.Entry(fenetre)
    entry_login.place(relx=0.5, rely=0.2, anchor="center")

    Label_mdp = tk.Label(fenetre, text="entrez votre mot de passe :")
    Label_mdp.place(relx=0.5, rely=0.4, anchor="center")
    entry_mdp = tk.Entry(fenetre, show="*")
    entry_mdp.place(relx=0.5, rely=0.5, anchor="center")

    submit= tk.Button(fenetre, text="se connecter", command=lambda:requete_connexion(fenetre, entry_login, entry_mdp))
    submit.place(relx=0.5, rely=0.7, anchor="center")


def page_connexion(windows):
    windows.destroy()
    fenetre=tk.Tk()
    fenetre.geometry('300x300')
    Label_login = tk.Label(fenetre, text="entrez votre pseudo  :")
    Label_login.place(relx=0.5, rely=0.1, anchor="center")
    entry_login = tk.Entry(fenetre)
    entry_login.place(relx=0.5, rely=0.2, anchor="center")

    Label_mdp = tk.Label(fenetre, text="entrez votre mot de passe :")
    Label_mdp.place(relx=0.5, rely=0.4, anchor="center")
    entry_mdp = tk.Entry(fenetre, show="*")
    entry_mdp.place(relx=0.5, rely=0.5, anchor="center")

    submit= tk.Button(fenetre, text="se connecter", command=lambda:requete_connexion(fenetre, entry_login, entry_mdp))
    submit.place(relx=0.5, rely=0.7, anchor="center")
    fenetre.mainloop()

#affiche le menu
def menu():
    fenetre=tk.Tk()
    fenetre.geometry("300x300")
    button_connecter= tk.Button(fenetre, text="se connecter", command=lambda :page_connexion(fenetre))
    button_connecter.pack()
    button_register= tk.Button(fenetre, text="se connecter", command=lambda :création_compte(fenetre))
    button_register.pack()
    # button_connecter= tk.Button(fenetre, text="Anonyme", command=connexion)
    # button_connecter.pack()
    fenetre.mainloop()
création_compte()