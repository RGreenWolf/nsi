import requests
import os
import json
import random
import unidecode

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

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_word(file_path, length=None, accents=True):
    try:
        file_path = f"./ressources/{file_path}"
        with open(file_path, 'r', encoding='utf-8') as file:
            words = json.load(file)
        
        if length is not None:
            words = [word for word in words if len(word) == length]
        
        if not accents:
            words = [word for word in words if word == unidecode.unidecode(word)]
        
        if not words:
            return None
        
        return random.choice(words)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None