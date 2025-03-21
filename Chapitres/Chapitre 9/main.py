def recherche_sequentielle(liste: list, x: int) -> bool:
    for num in liste:
        if num == x:
            return True
    return False

def recherche_dicotomique(liste: list, x: int) -> bool:
    debut, fin = 0, len(liste) - 1
    while debut <= fin:
        milieu = (debut + fin) // 2
        if liste[milieu] == x:
            return True
        elif liste[milieu] < x:
            debut = milieu + 1
        else:
            fin = milieu - 1
    return False