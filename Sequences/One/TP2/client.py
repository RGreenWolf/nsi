
import tkinter as tk
import requests


baseURL = "https://nsi.rgreenwolf.fr/mini-play/nombre"

def create_game(fenetre, canvas, labels, center_x, center_y):
    res = requests.post(baseURL + "/party/create", json={"player": "toto", "difficulty": "10"})
    #status
    if res.status_code == 200:
        id = res.json()['id']

        print(f"ID de la partie: {id}")

        new_game_id_label = tk.Label(fenetre, text=f"Nouvelle partie ID: {id}")
        canvas.create_window(center_x, center_y + 90 + len(labels) * 30, window=new_game_id_label)

        labels.append(new_game_id_label)
    else:
        print(f"Erreur: {res.status_code}")
    if res.json()['status'] != 'error':
        connecte = tk.Label(fenetre, text="tu es connecté")
        connecte.pack()
        fenetre.quit()
        jeu()

def join_party(fenetre, join, center_x, center_y):
    id = join.get()
    res = requests.post(baseURL + "/party/join", json={"player": "toto", "id": id})
    print(res.json()['status'])
    if res.json()['status'] != 'error':
        connecte = tk.Label(fenetre, text="tu es connecté")
        connecte.pack()
        fenetre.quit()
        jeu()
    else:
        print(f"Erreur: {res.json()['message']} ({res.status_code})")


# ATTENTION il faut faire en sorte quond puisse choisir son pseudi

#c'est super simple on le ferait après  
# OK

def jeu():
    print("faire l'interfae pour jouer")
    window=tk.Tk
    title = window.title("Mettez le nombre : ")
    title.pack()
    



def menu():
    fenetre = tk.Tk()
    fenetre.title("Deviner le nombre")
    canvas = tk.Canvas(fenetre, width=300, height=400)
    canvas.pack()

    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()
    center_x = canvas_width / 2
    center_y = canvas_height / 2

    labels = []

    start = tk.Button(fenetre, text="Commencer la partie", command=lambda : create_game(fenetre, canvas, labels, center_x, center_y))
    canvas.create_window(center_x, center_y + 30, window=start)

    join = tk.Entry(fenetre)
    join.pack()
    button_join= tk.Button(fenetre, text="join", command=lambda : join_party(fenetre, join, center_x, center_y))
    button_join.pack()

    code = tk.Entry(fenetre)
    canvas.create_window(center_x, center_y + 60, window=code)

    fenetre.mainloop()
menu()