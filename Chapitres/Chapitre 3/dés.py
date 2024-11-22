import random

lancers = [0] * 13
total_lancer = 10000

for _ in range(total_lancer):
    somme = random.randint(1, 6) + random.randint(1, 6)
    lancers[somme] += 1

print(lancers)

max_lancers = max(lancers[2:])
scale = 75 / max_lancers

for nombre in range(2, 13):
    etoiles = int(lancers[nombre] * scale)
    print(f"Nombre {nombre}: {lancers[nombre]} fois, Probabilité: {lancers[nombre] / total_lancer:.4f}  {'*' * etoiles}")
