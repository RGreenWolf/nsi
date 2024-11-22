import random

# initialisation
lancers = [0] * 13 # créer une liste de 13 éléments initialisés à 0
total_lancer = 10000 # nombre de lancers

for _ in range(total_lancer):
    # somme des dés
    somme = random.randint(1, 6) + random.randint(1, 6)
    lancers[somme] += 1

max_lancers = max(lancers[2:]) # nombre de fois que le nombre le plus fréquent a été lancé
scale = 75 / max_lancers # échelle pour afficher les étoiles

# print le nombre de fois que chaque nombre a été lancé
for nombre in range(2, 13):
    # etoiles = nombre d'étoiles correspondant au nombre de fois que le nombre a été lancé multiplié par l'échelle
    etoiles = int(lancers[nombre] * scale)
    # print imprimer le nombre d'étoiles correspondant au nombre de fois que le nombre a été lancé
    print(f"Nombre {nombre}: {lancers[nombre]} fois, Probabilité: {lancers[nombre] / total_lancer:.4f}  {'*' * etoiles}")