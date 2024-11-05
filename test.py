eleves = int(input("Nombre d'élèves: "))
initial = int(input("Nombre d'élèves initial: "))
oublie = int(input(""))
oublie = int(input(""))

def propagation_rumeur(n):
    u = initial
    for i in range (n):
        u = min(u*, 1000)
    return u

jour = 0
nb = 0
while nb <= eleves/2 :
    jour += 1
    nb = propagation_rumeur(jour)
    print(f"Jour {jour}: {nb} élèves")


print(f"plus de la moitié des élèves sont au courant de la rumeur au bout de {jour} jours")