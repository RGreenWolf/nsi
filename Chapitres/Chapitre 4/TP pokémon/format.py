import requests
import json

url = "https://tyradex.app/api/v1/pokemon"
response = requests.get(url)
pokemons_data = response.json()

def transformer_donnees(pokemon):
    if pokemon["pokedex_id"] == 0:
        return {}
    return {
        pokemon["name"]["fr"]: {
            "id": pokemon["pokedex_id"],
            "type": [t["name"] for t in pokemon["types"]],
            "stats": {
                "pv": pokemon["stats"]["hp"],
                "attaque": pokemon["stats"]["atk"],
                "defense": pokemon["stats"]["def"],
                "attaque_spe": pokemon["stats"]["spe_atk"],
                "defense_spe": pokemon["stats"]["spe_def"],
                "vitesse": pokemon["stats"]["vit"],
            },
            "faiblesse": [
                res["name"]
                for res in pokemon["resistances"]
                if res["multiplier"] > 1
            ],
            "evolution": pokemon["evolution"]["next"][0]["name"] if pokemon.get("evolution") and pokemon["evolution"]["next"] else None,
            "taille": float(pokemon["height"].replace(" m", "").replace(",", ".")),
            "poids": float(pokemon["weight"].replace(" kg", "").replace(",", ".")),
        }
    }


pokemons = {}
for pokemon in pokemons_data:
    pokemons.update(transformer_donnees(pokemon))

with open("pokemons.json", "w", encoding="utf-8") as fichier:
    json.dump(pokemons, fichier, ensure_ascii=False, indent=4)
