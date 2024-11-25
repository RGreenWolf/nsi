import tkinter as tk
import requests

baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"

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
        connecte = tk.Label(fenetre, text="Tu es connecté", fg="green", font=("Arial", 12))
        connecte.place(relx=0.5, rely=0.8, anchor="center")
        fenetre.quit()
        jeu(id, name)

# Fonction pour rejoindre une partie
def join_party(fenetre, join, name):
    id = join.get()
    name = name.get()
    res = requests.post(baseURL + "/party/join", json={"player": name, "id": id})
    if res.json()['status'] != 'error':
        connecte = tk.Label(fenetre, text="Tu es connecté", fg="green", font=("Arial", 12))
        connecte.place(relx=0.5, rely=0.8, anchor="center")
        fenetre.quit()
        jeu(id, name)
    else:
        print(f"Erreur: {res.json()['message']} ({res.status_code})")

# Fonction pour envoyer le résultat
def envoyer_result(window, nombre, id, name):
    resultat = nombre.get()
    if resultat.isdigit():
        print(f"le résultat est {resultat}")
        res = requests.post(baseURL + "/party/test", json={"id": id, "player": name, "num": resultat})
        print(res.text) #ici j'ai une erreru 500
    else:
        erreur = tk.Label(window, text="veuillez entrez un nombre")
        erreur.pack()

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

    window.mainloop()

# Interface du menu principal
def menu():
    fenetre = tk.Tk()
    fenetre.title("Deviner le nombre")
    fenetre.geometry("400x400")  # Taille de la fenêtre
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
    name_label = tk.Label(fenetre, text="Entrez l'ID de la partie :", bg="#f0f0f0", font=("Arial", 14))
    name_label.place(relx=0.5, rely=0.5, anchor="center")

    name_join = tk.Entry(fenetre, font=("Arial", 12), bd=2, relief="solid")
    name_join.place(relx=0.5, rely=0.6, anchor="center")

    join = tk.Entry(fenetre, font=("Arial", 12), bd=2, relief="solid")
    join.place(relx=0.5, rely=0.7, anchor="center")

    # Bouton pour rejoindre une partie
    button_join = tk.Button(fenetre, text="Rejoindre", command=lambda: join_party(fenetre, join, name_join),
                            font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=5)
    button_join.place(relx=0.5, rely=0.8, anchor="center")

    fenetre.mainloop()

menu()
