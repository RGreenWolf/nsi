tableau = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def aff_tab_1(tableau): 
    i = 0
    while i < len(tableau):
        print(tableau[i])
        i += 1

print("Exercice 1 :")
aff_tab_1(tableau)
print("\n")

def aff_tab_2(tableau): 
    for i in range(len(tableau)):
        print(tableau[i])

print("Exercice 2 :")
aff_tab_2(tableau)
print("\n")

def aff_tab_3(tableau):
    for i in tableau:
        print(i)

print("Exercice 3 :")
aff_tab_3(tableau)
print("\n")

def somme_pairs(tableau):
    somme = 0
    for i in range(len(tableau)):
        if tableau[i] % 2 == 0:
            somme += tableau[i]
    return somme

print("Exercice 4 :")
print(somme_pairs(tableau))
print("\n")

def minimun(tableau):
    min = tableau[0]
    for i in range(len(tableau)):
        if tableau[i] < min:
            min = tableau[i]
    return min

print("Exercice 5 :")
print(minimun(tableau))
print("\n")

def maximum(tableau):
    max = tableau[0]
    for i in range(len(tableau)):
        if tableau[i] > max:
            max = tableau[i]
    return max

print("Exercice 6 :")
print(maximum(tableau))
print("\n")


def moyenne(notes): return sum(notes) / len(notes)

notes = [15, 12, 18, 10, 14]
print("La moyenne est :", moyenne(notes))