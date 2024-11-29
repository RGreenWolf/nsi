# Exercice 1

print("Exercice 1")

chaine = "Le mot paix de par le monde"

print(len(chaine)) # pour les flemmards

len_chaine = 0
ord_chaine = []
for c in chaine :
    ord_chaine.append(ord(c))
    len_chaine += 1
print(len_chaine, ord_chaine)

# Exercice 2

print("\nExercice 2")

if "e" in chaine :
    print("e est dans la chaine")

for c in chaine:
    if c == "e" :
        print("e est dans la chaine")
        break

i = 0
stop = False
while i < len(chaine) and not stop:
    if chaine[i] == "e":
        print("e est dans la chaine")
        stop = True
    i += 1

# Exercice 3

print("\nExercice 3")

count_e = 0
for c in chaine:
    if c == "e":
        count_e += 1
print(f"Le caractère 'e' apparaît {count_e} fois dans la chaîne.")

# Exercice 4

print("\nExercice 4")

chaine = "EPID"
nouvelle_chaine = "*".join(chaine)
print(nouvelle_chaine)

# Exercice 5

print("\nExercice 5")

chaine = "zorglub"
nouvelle_chaine = chaine[::-1]
print(nouvelle_chaine)

# Exercice 6

print("\nExercice 6")

chaine = "radar"
if chaine == chaine[::-1]:
    print(f"La chaîne '{chaine}' est un palindrome.")
else:
    print(f"La chaîne '{chaine}' n'est pas un palindrome.")

def IsPalindrome(chaine: str) -> bool: return chaine == chaine[::-1] # fonctions en une ligne