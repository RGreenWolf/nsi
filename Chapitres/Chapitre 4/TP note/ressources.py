import json
import os
import requests

API = "https://api.younity-mc.fr/perso/nsi/mots/langues.json"
ressources = []

def download_ressource(url, path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(path, 'wb') as fichier:
            for chunk in response.iter_content(chunk_size=8192):
                fichier.write(chunk)
        
        print(f"Ressource téléchargée avec succès et sauvegardée à '{path}'")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")


def init_ressources():
    global ressources
    if not os.path.exists("./ressources"):
        os.makedirs("./ressources")

    ressources = requests.get(API).json()
    for i in ressources :
        pathFile = f"./ressources/{i["path"]}"
        if not os.path.exists(pathFile):
            download_ressource(i["url"], pathFile)
        with open(pathFile, "r", encoding="utf-8") as file:
            mots = json.load(file)
            print(f"Nombre de mots disponibles en {i["lang"]}: {len(mots)}")

def get_ressources_local(word=True):
    ressources = []
    if os.path.exists("./ressources"):
        for filename in os.listdir("./ressources"):
            pathFile = os.path.join("./ressources", filename)
            if os.path.isfile(pathFile):
                with open(pathFile, "r", encoding="utf-8") as file:
                    mots = json.load(file)
                    ressource = {
                        "lang": filename.replace(".json", "")
                    }
                    if word:
                        ressource["word"] = mots
                    ressources.append(ressource)
    return ressources