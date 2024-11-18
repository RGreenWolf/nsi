import random

tirages = [0] * 13
total_tirages = 10000

for _ in range(total_tirages):
    somme = random.randint(1, 6) + random.randint(1, 6)
    tirages[somme] += 1

for somme in range(2, 13):
    etoiles = tirages[somme] // 100
    print(f"Sommme {somme}: {tirages[somme]} fois, Probabilité: {tirages[somme] / total_tirages:.4f}  {'*' * etoiles}")
