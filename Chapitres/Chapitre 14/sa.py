objets_en_cale = [
    {"nom" : "malle d'or", "poids" : 150, "valeur" : 1500},
    {"nom" : "malle de perles", "poids" : 100, "valeur" : 800},
    {"nom" : "tonneau de rhum", "poids" : 40, "valeur" : 600},
    {"nom" : "malle de rubis", "poids" : 120, "valeur" : 2000},
    {"nom" : "malle de diamants", "poids" : 100, "valeur" : 25000},
    {"nom" : "malle d'épices", "poids" : 25, "valeur" : 3500},
    {"nom" : "coffre d'armes", "poids" : 120, "valeur" : 850},
    {"nom" : "tonneau de viandes séchées", "poids" : 10, "valeur" : 200},
    {"nom" : "sac de sels", "poids" : 10, "valeur" : 20},
    {"nom" : "malle de soie", "poids" : 50, "valeur" : 1000},
    {"nom" : "malle de vin", "poids" : 20, "valeur" : 300},
    {"nom" : "malle de fruits", "poids" : 30, "valeur" : 400},
    {"nom" : "tonneau de miel", "poids" : 15, "valeur" : 250},
    {"nom" : "coffre de bijoux", "poids" : 80, "valeur" : 5000},
    {"nom" : "malle de tissus", "poids" : 60, "valeur" : 1200},
    {"nom" : "tonneau d'huile", "poids" : 70, "valeur" : 900},
    {"nom" : "sac de café", "poids" : 20, "valeur" : 350},
    {"nom" : "coffre de chocolat", "poids" : 90, "valeur" : 1500},
    {"nom" : "malle de cuir", "poids" : 110, "valeur" : 2000},
    {"nom" : "tonneau de légumes", "poids" : 25, "valeur" : 300},
    {"nom" : "sac de sucre", "poids" : 15, "valeur" : 250},
    {"nom" : "coffre de fruits secs", "poids" : 35, "valeur" : 450}
]

def naif(objets, min=10):
    n=len(objets)
    combinaisons = []

    for i in range(2**n):
        combinaisons.append(bin(i)[2:].zfill(n))

    mini = float('inf')

    for combinaison in combinaisons:
        poids_jete = 0
        valeur_perdue = 0
        for j in range(n):
            if combinaison[j] == '1':
                poids_jete += objets[j]['poids']
                valeur_perdue += objets[j]['valeur']
        if poids_jete >= mini:
            print(f"Combinaison : {combinaison}, Poids jeté : {poids_jete}, Valeur perdue : {valeur_perdue}")
        

naif(objets_en_cale)