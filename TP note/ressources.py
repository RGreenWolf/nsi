import ultis
import json
import os
def ressources_manager(ressources):
    if not os.path.exists("./ressources"):
        os.makedirs("./ressources")
    for i in ressources :
        pathFile = f"./ressources/{i["path"]}"
        if not os.path.exists(pathFile):
            ultis.download_ressource(i["url"], pathFile)
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