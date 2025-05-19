import time
import itertools

objets_en_cale = [
    {"nom": "male d'or", "poids": 150, "valeur": 1500},
    {"nom": "male de perles", "poids": 100, "valeur": 800},
    {"nom": "tonneau de rhum", "poids": 40, "valeur": 600},
    {"nom": "male de rubis", "poids": 120, "valeur": 2000},
    {"nom": "male de diamants", "poids": 100, "valeur": 25000},
    {"nom": "male d'épices", "poids": 25, "valeur": 3500},
    {"nom": "coffre d'armes", "poids": 120, "valeur": 850},
    {"nom": "tonneau de viandes séchées", "poids": 10, "valeur": 200},
    {"nom": "sac de sels", "poids": 10, "valeur": 20},
    {"nom": "samsung-galaxy_a21s", "poids": 50, "valeur": 250},
    {"nom": "amd_ryzen_7_3600gb", "poids": 100, "valeur": 500},
    {"nom": "nuage", "poids": 100, "valeur": 10},
    {"nom": "coffre poudre noir", "poids": 150, "valeur": 900},
    {"nom": "boussole", "poids": 10, "valeur": 2000},
    {"nom": "cheval", "poids": 250, "valeur": 1000},
    {"nom": "singe", "poids": 10, "valeur": 20},
    {"nom": "malle de carte", "poids": 10, "valeur": 50},
    {"nom": "longue vue", "poids": 20, "valeur": 80},
    {"nom": "jack sparrow", "poids": 80, "valeur": 10},
    {"nom": "relique magique", "poids": 40, "valeur": 1000000},
    {"nom": "coca_cola_light", "poids": 33, "valeur": 1},
    {"nom": "Kalachnikov", "poids": 5, "valeur": 2500},
    {"nom": "Sac de poireaux", "poids": 15, "valeur": 30},
    {"nom": "Fiat Multipla", "poids": 250, "valeur": 15000},
]

def meilleur_ratio(objets: list, poids_min: int = 10):
    n = len(objets)
    meilleures_combis = []

    for k in range(1, n+1):
        for combinaison in itertools.combinations(objets, k):
            poids_total = sum(obj['poids'] for obj in combinaison)
            valeur_totale = sum(obj['valeur'] for obj in combinaison)
            if poids_total >= poids_min:
                ratio = valeur_totale / poids_total
                meilleures_combis.append((poids_total, valeur_totale, [obj['nom'] for obj in combinaison], ratio))

    if not meilleures_combis:
        return None

    # On trie par ratio croissant
    meilleures_combis.sort(key=lambda x: x[3])
    return meilleures_combis[-1]  # Meilleur ratio

start = time.time()
solution = meilleur_ratio(objets_en_cale, poids_min=100)
end = time.time()
print(f"Temps d'exécution : {end - start:.2f} secondes")

if solution:
    poids, valeur, objets, ratio = solution
    print(f"Object total : {len(objets_en_cale)}")
else:
    print("Aucune combinaison ne satisfait le poids minimum.")

