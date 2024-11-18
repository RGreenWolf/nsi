# import
import time
import sys
from random import shuffle, choice, randint
import os

# constants
MAX_BOULES = 50
ANNIMATION_BOULES = 30
ANNIMATION_TIMES = 0.05
TIRAGE_BOULES = 5

def creer_boules():
    return list(range(1, MAX_BOULES + 1))

# init
boules = creer_boules()
tirage = []
choice_boules = []
affichage = [0] * TIRAGE_BOULES

def brassage(tirage_num, boules):
    for _ in range(ANNIMATION_BOULES):
        affichage[tirage_num] = randint(1, MAX_BOULES)
        affichage_str = " ".join([f"{num:02d}" for num in affichage])
        sys.stdout.write(f"\r{affichage_str}   ")
        sys.stdout.flush()
        time.sleep(ANNIMATION_TIMES)
        shuffle(boules)

def tirage_boules():
    boule = choice(boules)
    boules.remove(boule)
    tirage.append(boule)
    return boule

def affichages(tirage_num, boule):
    affichage[tirage_num] = boule
    affichage_str = " ".join([f"{num:02d}" for num in affichage])
    sys.stdout.write(f"\r{affichage_str}   ")
    sys.stdout.flush()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_resulat():
    clear_screen()
    print("\nLes boules tirées sont : ", " | ".join(map(str, tirage)) + " |")
    if tirage == choice_boules:
        print("Vous avez gagné !")
    else:
        print("\033[31mVous avez perdu !\033[0m")
        print("\033[31mQuelle dommage !\033[0m")
        print("\033[31mOn ne si attendait pas !\033[0m")
        print("\033[31mIl ne faut pas jouer à la loterie, ses stupides les chances de gagner sont de 0,00000002% !\033[0m")
        print("\033[31mC'est une arnaque !\033[0m")
        print("\033[31mPlus de chance de se faire frapper par la foudre !\033[0m")


def choix_boules():
    for _ in range(TIRAGE_BOULES):
        while True:
            try:
                boule = int(input(f"Entrez le numéro {_+1} compris entre 1 et {MAX_BOULES} : "))
                if 1 <= boule <= MAX_BOULES:
                    choice_boules.append(boule)
                    clear_screen()
                    break
                else:
                    print(f"Le numéro doit être compris entre 1 et {MAX_BOULES}.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre entier.")

# main
def start(): 
    choix_boules()
    for tirage_num in range(TIRAGE_BOULES):
        brassage(tirage_num, boules)
        boule = tirage_boules()
        affichages(tirage_num, boule)
        time.sleep(1)
    afficher_resulat()

if __name__ == "__main__":
    start()