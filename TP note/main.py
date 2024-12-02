import annimation
import ultis
from ressources import ressources_manager, get_ressources_local
import sys

ressources = [
    {
        "lang": "francais",
        "path": "francais.json",
        "url": "https://raw.githubusercontent.com/words/an-array-of-french-words/refs/heads/master/index.json"
    },
    {
        "lang": "english",
        "path": "english.json",
        "url": "https://raw.githubusercontent.com/words/an-array-of-english-words/refs/heads/master/index.json"
    },
    {
        "lang": "spanish",
        "path": "spanish.json",
        "url": "https://raw.githubusercontent.com/words/an-array-of-spanish-words/refs/heads/master/index.json"
    }
]

liste = []
debugMode = True if "--dev" in sys.argv else False
langue = "francais"

def play(lettre, mot, liste):
    trouve = False
    for i in range(len(mot)):
        if mot[i] == lettre:
            liste[i] = lettre
            trouve = True
    return trouve

def pendu(mot):
    liste = []
    for i in range(len(mot)):
        liste.append("_")
    
    tentative = len(annimation.pendu_animation)
    while "_" in liste and tentative != 0:
        print(" ".join(liste))
        lettre = input("Proposer une lettre ? ")
        if not play(lettre, mot, liste):
            tentative -= 1
            print(annimation.pendu_animation[::-1][tentative])
        print(f"Tentatives restantes: {tentative}")

    if "_" in liste:
        return False
    return True

def choisir_mot():
    global langue
    print("Choisissez un type de mot :")
    print("1. Mot personnalisé")
    print("2. Mot aléatoire")
    choix = input("Votre choix : ")
    if choix == "1":
        mot = input("Entrez le mot à deviner : ")
    elif choix == "2":
        print("Paramètres pour le mot aléatoire :")
        longueur = int(input("Longueur minimale du mot : "))
        accents = input("Autoriser les accents ? (oui/non) : ").strip().lower() == "oui"
        ressource_path = f"{langue}.json"
        mot = ultis.get_random_word(ressource_path, longueur, accents)
        if debugMode:
            print(f"TRICHE : {mot}")
    else:
        print("Option invalide, veuillez réessayer.")
        return choisir_mot()
    return mot

def menu():
    stop = False
    while not stop:
        if not debugMode:
            ultis.clear_console()
        print("1. Jouer")
        print("2. Paramètres")
        print("3. Quitter")
        choix = input("Choisissez une option : ")
        if choix == "1":
            mot = choisir_mot()
            if pendu(mot):
                print("Félicitations, vous avez gagné !")
            else:
                print(f"Dommage, vous avez perdu. Le mot était : {mot}")
        elif choix == "2":
            menu_parametres()
        elif choix == "3":
            print("Au revoir !")
            stop = True
        else:
            print("Option invalide, veuillez réessayer.")

def menu_parametres():
    global langue
    print("Paramètres :")
    print("1. Changer de langue")
    print("2. Retour")
    choix = input("Votre choix : ")
    if choix == "1":
        print("Langues disponibles :")
        langues_disponibles = get_ressources_local(False)
        for idx, lang in enumerate(langues_disponibles):
            print(f"{idx + 1}. {lang['lang']}")
        langue_choix = input("Choisissez une langue : ")
        try:
            index = int(langue_choix) - 1
            if 0 <= index < len(langues_disponibles):
                langue = langues_disponibles[index]['lang']
                print(f"Langue changée en : {langue}")
            else:
                print("Option invalide.")
        except ValueError:
            print("Option invalide.")
    elif choix != "2":
        print("Option invalide.")


def main():
    ultis.clear_console()
    print("Chargement en cours...")
    ressources_manager(ressources)
    print("Chargement terminé !")
    menu()

main()
