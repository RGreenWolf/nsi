import os
import json
import random
import unidecode

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

import random
import json
from unidecode import unidecode

def get_random_word(file_path, length=None, accents=True):
    try:
        file_path = f"./ressources/{file_path}"
        with open(file_path, 'r', encoding='utf-8') as file:
            words = json.load(file)

        if length is not None:
            while length > 0:
                filtered_words = [
                    word for word in words
                    if len(word) == length and (accents or word == unidecode(word))
                ]
                
                if filtered_words:
                    return random.choice(filtered_words)
                
                length -= 1
        
        filtered_words = [
            word for word in words
            if accents or word == unidecode(word)
        ]
        return random.choice(filtered_words) if filtered_words else None

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None
