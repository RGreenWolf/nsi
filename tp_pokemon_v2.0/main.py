####################################################################
###### TP POKEMONS V2.0                                 ############
###### AUTEUR : Van Uytvanck Nathan                     ############
###### DATE : 20/01/2025                                ############
####################################################################

####################################################################
# 1. Créer la fonction importation(fichier) qui permet de retourner
#  un dictionnaire de dictionnaires. Chaque dictionnaire est associé 
# à une clé: le nom du pokémon et toutes les informations de chaque pokémon
# se trouvent dans le sous-dictionnaire(Reprendre la v1.0 de pokémon)
def importation(fichier):
    file = open(fichier, "r", encoding="utf8")
    table = {}

    descripteurs = file.readline().rstrip().split(",")
    for line in file.readlines():
        values = line.rstrip().split(",")
        table[values[1]] = {descripteurs[i]: values[i] for i in range(0, len(descripteurs))}
    file.close()
    return table

####################################################################


####################################################################
# 2. Reprendre les différentes fonctions de la v1.0 et modifier en conséquence
# les fonctions de recherche, d'affichage et d'ajout
def afficherPokemon(pokemon:dict):
    print("**********")
    for (key, value) in pokemon.items():
        print(f"{key} : {value}")
    print("**********")


def afficherPokemons():
    for pokemon in pokemons.values():
        afficherPokemon(pokemon=pokemon)

def ajouterPokemon(new_pokemon:dict):
    if new_pokemon["Name"] in pokemons:
        print("Le Pokémon existe déjà dans le fichier CSV.")
        return
    pokemons[new_pokemon["Name"]] = new_pokemon
    with open("pokemon.csv", "a", encoding="utf8") as file:
        file.write(",".join(new_pokemon.values()) + "\n")
    print("Nouveau Pokémon ajouté au fichier CSV.")

####################################################################

####################################################################
# 3. Écrire une fonction pokemonEau() permettant de retourner
# la liste des noms des Pokémons de type Eau (Water dans le CSV)
def pokemonEau():
    resultats = [
        pokemon["Name"] for pokemon in pokemons.values() if pokemon["Type_1"] == "Water" or pokemon["Type_2"] == "Water"
    ]
    return resultats

####################################################################

####################################################################

# 4. Écrire une fonction pokemonMore50HP() permettant de
#  retourner la liste les noms des Pokémons de plus de 50HP

def pokemonMore50HP():
    resultats = [
        pokemon["Name"] for pokemon in pokemons.values() if int(pokemon["HP"]) > 50
    ]
    return resultats

####################################################################

####################################################################
# 5. Ecrire une fonction filtre(critere, val) qui prend en paramètre
#  critere (un descripteur existant dans le dictionnaire) et val 
# la valeur du critère et qui retourne la liste des noms de pokémons qui correspondent au critère.
def filtre(critere, val):
    resultats = [
        pokemon["Name"] for pokemon in pokemons.values() if pokemon[critere] == val
    ]
    return resultats

####################################################################    

####################################################################
# 6. Ecrire une fonction tri() qui prend en paramètre
#  critere (un descripteur existant dans le dictionnaire) et qui retourne
#  la liste des noms de pokémons triés par ordre croissant du nom.
def tri():
    return sorted(pokemons.keys())

####################################################################

# 7. Écrire une fonction doublons permettant de rechercher 
# les doublons ID(  # ) de Pokémon dans la table pokemon.csv, ici 
#     l'algorithme retourne une liste de tuples :  les doublons : l’ID (#) et le nom du pokémon
def doublons():
    resultats = []
    for pokemon in pokemons.values():
        for pokemonTest in pokemons.values():
            if pokemon["#"] == pokemonTest["#"] and pokemon["Name"] != pokemonTest["Name"]:
                resultats.append((pokemon["#"], pokemon["Name"]))
    return resultats

############ ZONE D'APPELS (prints)  ############
# # Question 1
# print("**** QUESTION 1 ****")
# pokemons = importation("pokemon.csv")

# # Question 2
# print("**** QUESTION 2 ****")
# # Afficher Pikachu avec toutes ses infos
# afficherPokemon(pokemons["Pikachu"])
# # Afficher tous les pokemons
# afficherPokemons(pokemons)

# # Ajoute un pokemon bidon (Hulk)
# ajouterPokemon({
#     "#": "999",
#     "Name": "Hulk",
#     "Type_1": "Normal",
#     "Type_2": "Grass",
#     "Total": "600",
#     "HP": "200",
#     "Attack": "80",
#     "Defense": "120",
#     "Sp_Atk": "50",
#     "Sp_Def": "50",
#     "Speed": "100",
#     "Generation": "Avengers",
#     "Legendary": "True",
#     "Evolution": "Mega-Hulk"
# })

# # Question 3
# print("**** QUESTION 3 ****")
# print(pokemonEau(), "\nIl y a ", len(pokemonEau()), "pokémons de type Eau")

# # Question 4
# print("**** QUESTION 4 ****")
# print(pokemonMore50HP(), "\nIl y a ", len(pokemonMore50HP()), "pokémons de plus de 50HP")

# #Question 5
# print("**** QUESTION 5 ****")
# print(filtre("Type_1", "Water"), "\nIl y a ", len(filtre("Type_1", "Water")), "pokémons de type 1 Eau")
# print(filtre("Type_2", "Water"), "\nIl y a ", len(filtre("Type_2", "Water")), "pokémons de type 2 Eau")
# print(filtre("Generation", "1"), "\nIl y a ", len(filtre("Generation", "1")), "pokémons de la génération 1")
# print(filtre("Legendary", "True"), "\nIl y a ", len(filtre("Legendary", "True")), "pokémons légendaires")

# # Question 6
# print("**** QUESTION 6 ****")
# print(tri())

# # Question 7
# print("**** QUESTION 7 ****")
# print(doublons())
# print("Il y a ", len(doublons()), " doublons au total.")

############ ZONE DE TESTS  ############
pokemons = importation("pokemon.csv")
assert pokemons["Pikachu"] == {'#': '25', 'Name': 'Pikachu', 'Type_1': 'Electric', 'Type_2': '', 'Total': '320', 'HP': '35', 'Attack': '55', 'Defense': '40', 'Sp_Atk': '50', 'Sp_Def': '50', 'Speed': '90', 'Generation': '1', 'Legendary': 'False', 'Evolution': 'Raichu'}, "Erreur avec l'importation"
afficherPokemon(pokemons["Pikachu"])
afficherPokemons()
ajouterPokemon({
    "#": "999",
    "Name": "Hulk",
    "Type_1": "Normal",
    "Type_2": "Grass",
    "Total": "600",
    "HP": "200",
    "Attack": "80",
    "Defense": "120",
    "Sp_Atk": "50",
    "Sp_Def": "50",
    "Speed": "100",
    "Generation": "Avengers",
    "Legendary": "True",
    "Evolution": "Mega-Hulk"
})
assert pokemons["Hulk"] == {'#': '999', 'Name': 'Hulk', 'Type_1': 'Normal', 'Type_2': 'Grass', 'Total': '600', 'HP': '200', 'Attack': '80', 'Defense': '120', 'Sp_Atk': '50', 'Sp_Def': '50', 'Speed': '100', 'Generation': 'Avengers', 'Legendary': 'True', 'Evolution': 'Mega-Hulk'}, "Erreur lors de l'ajout de Hulk"

assert len(pokemonEau()) == 34, "Erreur avec le nombre de pokémons de type eau"

assert len(pokemonMore50HP()) == 110, "Erreur avec le nombre de pokémons de + de 50HP (comptant Hulk)"

assert len(filtre("Type_1", "Water")) == 30, "Erreur avec le nombre de pokémons de type1 eau (comptant Hulk)"
assert len(filtre("Type_2", "Water")) == 4, "Erreur avec le nombre de pokémons de type2 eau (comptant Hulk)"
assert len(filtre("Generation", "1")) == 162, "Erreur avec le nombre de pokémons génération 1 (comptant Hulk)"
assert len(filtre("Legendary", "True")) == 7, "Erreur avec le nombre de pokémons légendaires (comptant Hulk)"

assert tri()[0] == 'Abra', "Erreur avec la fonction tri()"

assert len(doublons()) == 26, "Erreur avec la fonction doublons"