import json
import matplotlib.pyplot as plt

def readFile():
    with open("pays.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


pays = readFile()

def saveFile():
    with open("pays.json", "w") as file:
        json.dump(pays, file)

def addPays(nom, capitale):
    for p in pays:
        if p["nom"] == nom:
            print("Le pays existe déjà")
            return p
    pays.append({"nom": nom, "capitale": capitale["nom"], "villes": [capitale]})
    saveFile()

addPays("Belgique", {
    "nom": "Bruxelles",
    "region": "Bruxelles-Capitale",
    "population": 185103
})

def addVille(nomPays, ville):
    for p in pays:
        if p["nom"] == nomPays:
            for v in p["villes"]:
                if v["nom"] == ville["nom"]:
                    print("La ville existe déjà")
                    return v
            p["villes"].append(ville)
            saveFile()

def get_villes_by_pays(nomPays):
    for p in pays:
        if p["nom"] == nomPays:
            return p["villes"]
    return []

def get_ville_by_nom(nomVille):
    for p in pays:
        for v in p["villes"]:
            if v["nom"] == nomVille:
                return v
    return None

def get_pays_with_max_villes():
    max_villes = 0
    pays_max_villes = None
    for p in pays:
        if len(p["villes"]) > max_villes:
            max_villes = len(p["villes"])
            pays_max_villes = p
    return pays_max_villes

def get_population_mondiale():
    population = 0
    for p in pays:
        for v in p["villes"]:
            population += v["population"]
    return population

def get_population_pays(nomPays):
    for p in pays:
        if p["nom"] == nomPays:
            population = 0
            for v in p["villes"]:
                population += v["population"]
            return population
    return None

def afficher_carte_mondiale():
    points = []
    
    for p in pays:
        for v in p["villes"]:
            if "coordonnees" in v and "latitude" in v["coordonnees"] and "longitude" in v["coordonnees"]:
                latitude = v["coordonnees"]["latitude"]
                longitude = v["coordonnees"]["longitude"]
                points.append((latitude, longitude))
    
    if points:
        latitudes = [point[0] for point in points]
        longitudes = [point[1] for point in points]

        plt.figure(figsize=(15, 10))
        plt.scatter(longitudes, latitudes, c='blue', alpha=0.6, s=10)
        plt.title("Carte du monde avec les villes")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        plt.show()
    else:
        print("Aucune donnée géographique disponible.")


def afficher_menu():
    print("1. Ajouter un pays")
    print("2. Ajouter une ville")
    print("3. Afficher les villes d'un pays")
    print("4. Rechercher une ville par son nom")
    print("5. Afficher la mondiale en carte")
    print("6. Quitter")

while True:
    afficher_menu()
    choix = input("Choisissez une option: ")
    
    if choix == "1":
        nom = input("Nom du pays: ")
        capitale_nom = input("Nom de la capitale: ")
        capitale_region = input("Région de la capitale: ")
        capitale_population = int(input("Population de la capitale: "))
        addPays(nom, {
            "nom": capitale_nom,
            "region": capitale_region,
            "population": capitale_population
        })
    elif choix == "2":
        nomPays = input("Nom du pays: ")
        ville_nom = input("Nom de la ville: ")
        ville_region = input("Région de la ville: ")
        ville_population = int(input("Population de la ville: "))
        addVille(nomPays, {
            "nom": ville_nom,
            "region": ville_region,
            "population": ville_population
        })
    elif choix == "3":
        nomPays = input("Nom du pays: ")
        villes = get_villes_by_pays(nomPays)
        if villes:
            for ville in villes:
                print(ville["nom"])
        else:
            print("Le pays n'existe pas")
    elif choix == "4":
        nomVille = input("Nom de la ville: ")
        ville = get_ville_by_nom(nomVille)
        if ville:
            for key, value in ville.items():
                print(f"{key}: {value}")
        else:
            print("La ville n'existe pas")
    elif choix == "5":
        afficher_carte_mondiale()
    elif choix == "6":
        break
    else:
        print("Choix invalide")