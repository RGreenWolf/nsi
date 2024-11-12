# utils.py
import os

def create_file_if_not_exists(key, default):
    if not os.path.exists(key):
        with open(key, 'w') as file:
            file.write(default)
        print(f"Fichier '{key}' créé avec le contenu par défaut.")

def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Dossier '{folder}' créé.")