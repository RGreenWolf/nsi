def exercice_1():
    A = 5
    B = 3
    C = A + B
    A = 2
    C = B - A
    print(A)
    print(B)
    print(C)

def exercice_2():
    A = 2
    B = 1
    C = 6
    B = A
    C = B
    A = C
    print(A, B, C)

def exercice_3():
    val = 6
    leDouble = 2 * val
    print(leDouble)

def exercice_4():
    num = int(input("Entrez un nombre: "))
    carre = num ** 2
    print(f"Le carré de {num} est {carre}")

def exercice_5():
    prenom = input("Entrez votre prénom :")
    print(f"Bonjour {prenom}")

def exercice_6():
    def calculer_prix_ttc(prix_ht, quantite, taux_tva):
        montant_tva = prix_ht * (taux_tva / 100)
        prix_ttc_article = prix_ht + montant_tva
        prix_total_ttc = prix_ttc_article * quantite
        return prix_total_ttc

    prix_ht = float(input("Entrez le prix HT de l'article : "))
    quantite = int(input("Entrez le nombre d'articles : "))
    taux_tva = float(input("Entrez le taux de TVA (en %) : "))

    prix_total_ttc = calculer_prix_ttc(prix_ht, quantite, taux_tva)

    print(f"\nPrix total TTC pour {quantite} article(s) à {prix_ht}€ HT avec un taux de TVA de {taux_tva}% : {prix_total_ttc:.2f}€")

def exercice_7():
    nombre = float(input("Entrez un nombre : "))
    if nombre > 0:
        print("Le nombre est positif.")
    elif nombre < 0:
        print("Le nombre est négatif.")
    else:
        print("Le nombre est zéro.")

def exercice_8():
    age = int(input("Entrez l'âge de l'enfant : "))
    if 6 <= age <= 7:
        print("Catégorie : Poussin")
    elif 8 <= age <= 9:
        print("Catégorie : Pupille")
    elif 10 <= age <= 11:
        print("Catégorie : Minime")
    elif age >= 12:
        print("Catégorie : Cadet")
    else:
        print("Âge non valide.")

def exercice_9():
    max = int(input("Entrez un nombre maximal : "))
    min = int(input("Entrez un nombre minimal : "))
    for i in range(min, max+1):
        print(i)

def exercice_10():
    max = int(input("Entrez un nombre maximal : "))
    min = int(input("Entrez un nombre minimal : "))
    res = []
    for i in range(min, max+1):
        if i % 2 == 0:
            res.append(i)
    print(res)

def exercice_11():
    max = int(input("Entrez un nombre maximal : "))
    min = int(input("Entrez un nombre minimal : "))
    res = []

    def nombreBetween(min, max):
        for i in range(min, max+1):
            if i % 2 == 0:
                res.append(i)
        return res

    print(nombreBetween(min, max))

def exercice_12():
    def table_multiplication(nombre):
        print(f"Table de multiplication de {nombre} :")
        for i in range(1, 11):
            resultat = nombre * i
            print(f"{nombre} x {i} = {resultat}")

    nombre = int(input("Entrez le nombre que vous voulez afficher la table de multiplication : "))
    table_multiplication(nombre)

def exercice_13():
    print("🍃🏜️", "\nIl n'y a pas grand chose ici...")

def exercice_14():
    import math
    print("Exercice de satan 😈 !")
    def equation_second_degre(a, b, c):
        delta = b**2 - 4*a*c
        print("Delta =", delta)
        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
            print("L'équation a deux solutions réelles distinctes : x1 =", x1, ", x2 =", x2)
        elif delta == 0:
            x = -b / (2 * a)
            print("L'équation a une solution réelle double : x =", x)
        else:
            print("L'équation n'a pas de solution réelle.")
        
    a = float(input("Entrez le coefficient a : "))
    b = float(input("Entrez le coefficient b : "))
    c = float(input("Entrez le coefficient c : "))
    equation_second_degre(a, b, c)


def exercice_15():
    import math

    def calculatrice():
        premier_nombre = float(input("Entrez le premier nombre : "))
        deuxieme_nombre = float(input("Entrez le deuxième nombre : "))
        operation = input("Choix de l'opération (+, -, *, /, ** pour puissance, sqr pour racine carrée) : ")

        if operation == '+':
            resultat = premier_nombre + deuxieme_nombre
            print(f"Le résultat de {premier_nombre} + {deuxieme_nombre} est égal à {resultat}")
        elif operation == '-':
            resultat = premier_nombre - deuxieme_nombre
            print(f"Le résultat de {premier_nombre} - {deuxieme_nombre} est égal à {resultat}")
        elif operation == '*':
            resultat = premier_nombre * deuxieme_nombre
            print(f"Le résultat de {premier_nombre} * {deuxieme_nombre} est égal à {resultat}")
        elif operation == '/':
            if deuxieme_nombre != 0:
                resultat = premier_nombre / deuxieme_nombre
                print(f"Le résultat de {premier_nombre} / {deuxieme_nombre} est égal à {resultat}")
            else:
                print("Erreur : Division par zéro.")
        elif operation == '**':
            resultat = premier_nombre ** deuxieme_nombre
            print(f"Le résultat de {premier_nombre} puissance {deuxieme_nombre} est égal à {resultat}")
        elif operation == 'sqr':
            resultat = math.sqrt(premier_nombre)
            print(f"La racine carrée de {premier_nombre} est égal à {resultat}")
        else:
            print("Opération non valide.")
        
        reponse = input("Voulez-vous effectuer un autre calcul ?\n Oui/Non :")
        if reponse.lower() == 'oui':
            calculatrice()
        else:
            print("Au revoir !")

    calculatrice()

def exercice_16():
    import random
    matchs = []
    def replay():
        reponse = input("Voulez-vous rejouer ?\n Oui/Non :")
        if reponse.lower() == 'oui':
            play()
        elif reponse.lower() == 'non':
            print("Voici le récapitulatif des matchs :" )
            for match in matchs:
                print("- " + match)
            print("Au revoir !")
    def play():
        options = ["pierre", "papier", "ciseau"]
        choixOrdi = random.choice(options)
        choixJoueur = input("Entrez votre choix (pierre, papier, ciseau) : ").lower()
        if choixJoueur in options:
            print(f"Le choix de l'ordinateur est : {choixOrdi}")
            if choixJoueur == choixOrdi:
                print("Egalité !")
                status = "egalite"
            elif (choixJoueur == "pierre" and choixOrdi == "ciseau") or (choixJoueur == "papier" and choixOrdi == "pierre") or (choixJoueur == "ciseau" and choixOrdi == "papier"):
                print("Vous avez gagné !")
                status = "win"
            else:
                print("Vous avez perdu !")
                status = "perdu"
            matchs.append(status)
            replay()
        else :
            print("Choix non valide, veuillez réessayer.")
            replay()
    play()



exercices = {
    '1': exercice_1,
    '2': exercice_2,
    '3': exercice_3,
    '4': exercice_4,
    '5': exercice_5,
    '6': exercice_6,
    '7': exercice_7,
    '8': exercice_8,
    '9': exercice_9,
    '10': exercice_10,
    '11': exercice_11,
    '12': exercice_12,
    '13': exercice_13,
    '14': exercice_14,
    '15': exercice_15,
    '16': exercice_16,
}

print("Choisissez un exercice à exécuter :")
choix = input("Votre choix : ")
if exercices.get(choix):
    exercices[choix]() 
else:
    print("Choix non valide, veuillez réessayer.")
