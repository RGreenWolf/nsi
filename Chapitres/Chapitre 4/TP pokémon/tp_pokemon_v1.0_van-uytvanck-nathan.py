pokemons = {
    "bulbizarre": {
        "id": 1,
        "type": [
            "Plante",
            "Poison"
        ],
        "stats": {
            "pv": 45,
            "attaque": 49,
            "defense": 49,
            "attaque_spe": 65,
            "defense_spe": 65,
            "vitesse": 45,
        },
        "faiblesse": [
            "Feu",
            "Glace",
            "Vol",
            "Psy"
        ],
        "evolution": "herbizarre",
        "taille": 0.7,
        "poids": 6.9,
    },
    "arceus": {
        "id": 493,
        "name": "Arceus",
        "type": [
            "Normal"
        ],
        "stats": {
            "pv": 120,
            "attaque": 120,
            "defense": 120,
            "attaque_spe": 120,
            "defense_spe": 120,
            "vitesse": 120,
        },
        "faiblesse": [
            "Combat"
        ],
        "evolution": None,
        "taille": 3.2,
        "poids": 320,
    }
}

def add_pokemon(name, id, type=["Normal"], stats=None, faiblesse=["Aucune"], evolution=None, taille=0.0, poids=0.0):
    pokemons[name] = {
        "id": id,
        "type": type,
        "stats": stats,
        "faiblesse": faiblesse,
        "evolution": evolution,
        "taille": taille,
        "poids": poids,
    }
    return True

def show_pokemon(name):
    pokemon = pokemons.get(name, None)
    if pokemon is None:
        print(f"Le pokémon {name} n'existe pas.")
        return
    print(f"\nInformations du pokémon {name}: ")
    print(f"ID: {pokemon['id']}")
    print(f"Type: {', '.join(pokemon['type'])}")
    print(f"Faiblesse: {', '.join(pokemon['faiblesse'])}")
    print("Stats:")
    for stat, value in pokemon['stats'].items():
        print(f"  {stat.replace('_', ' ').capitalize()}: {value}")
    print(f"Évolution: {pokemon['evolution'] if pokemon['evolution'] else 'Aucune'}")
    print(f"Taille: {pokemon['taille']} m")
    print(f"Poids: {pokemon['poids']} kg")

def show_all_pokemons():
    for name in pokemons:
        show_pokemon(name)

def search_pokemon(search):
    for name in pokemons:
        if search.lower() in name.lower() or (search.isdigit() and pokemons[name]['id'] == int(search)):
            return name 
    return None

def main():
    running = True
    while running:
        print("\n1. Ajouter un pokémon")
        print("2. Recherche un pokémon")
        print("3. Afficher tous les pokémons")
        print("4. Quitter")
        choice = input("Que voulez-vous faire ? ")
        if choice == "1":
            name = input("Nom: ")
            id = int(input("ID: "))
            type = input("Type (séparés par des virgules): ").split(",")
            stats = {
                "pv": int(input("PV: ")),
                "attaque": int(input("Attaque: ")),
                "defense": int(input("Défense: ")),
                "attaque_spe": int(input("Attaque spéciale: ")),
                "defense_spe": int(input("Défense spéciale: ")),
                "vitesse": int(input("Vitesse: ")),
            }
            faiblesse = input("Faiblesses (séparées par des virgules): ").split(",")
            evolution = input("Évolution: ")
            taille = float(input("Taille (en mètres): "))
            poids = float(input("Poids (en kg): "))
            res = add_pokemon(name, id, type, stats, faiblesse, evolution, taille, poids)
            if res:
                print(f"Le pokémon {name} a bien été ajouté.")
            else:
                print(f"Erreur lors de l'ajout du pokémon {name}.")
        elif choice == "2":
            search = input("Recherche: ")
            pokemon = search_pokemon(search)
            if pokemon is None:
                print(f"Le pokémon {search} n'existe pas.")
            else:
                show_pokemon(search)
        elif choice == "3":
            show_all_pokemons()
        elif choice == "4":
            running = False
        else:
            print("Choix invalide.")

main()

