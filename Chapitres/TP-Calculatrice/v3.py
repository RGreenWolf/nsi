import tkinter as tk
from tkinter import ttk, messagebox

# Dictionnaire pour la conversion hexadécimale
hexToBinDict = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111"
}

# Conversion binaire -> décimal
def binToDec(nombre_bin):
    if nombre_bin[0] == "1" and len(nombre_bin) > 1:
        taille = len(nombre_bin)
        return int(nombre_bin, 2) - (1 << taille)
    return int(nombre_bin, 2)  # Positif

# Conversion décimal -> binaire
def decToBin(nombre_dec):
    if nombre_dec < 0:
        nb_complement_2 = (1 << 8) + nombre_dec
        return bin(nb_complement_2)[2:].zfill(8)
    return bin(nombre_dec)[2:]  # Positif

# Conversion décimal -> hexadécimal
def decToHex(nombre_dec):
    if nombre_dec < 0:
        raise ValueError("Les nombres négatifs ne sont pas pris en charge pour le format hexadécimal.")
    return hex(nombre_dec)[2:].upper()

# Conversion binaire -> hexadécimal
def binToHex(nombre_bin):
    if nombre_bin[0] == "1" and len(nombre_bin) > 1:
        raise ValueError("Les nombres binaires négatifs ne sont pas pris en charge pour le format hexadécimal.")
    while len(nombre_bin) % 4 != 0:
        nombre_bin = "0" + nombre_bin
    return "".join(
        key for i in range(0, len(nombre_bin), 4)
        for key, value in hexToBinDict.items() if value == nombre_bin[i:i+4]
    )

# Conversion hexadécimal -> binaire
def hexToBin(nombre_hex):
    return "".join(hexToBinDict[char] for char in nombre_hex.upper())

# Conversion hexadécimal -> décimal
def hexToDec(nb_hex):
    return int(nb_hex, 16)

def calculer_resultat():
    try:
        base = base_selectionnee.get()
        operation = operation_selectionnee.get()

        if base == "2":
            nombre1 = int(entree_nombre1.get(), 2)
            nombre2 = int(entree_nombre2.get(), 2)
        elif base == "10":
            nombre1 = int(entree_nombre1.get(), 10)
            nombre2 = int(entree_nombre2.get(), 10)
        elif base == "16":
            nombre1 = int(entree_nombre1.get(), 16)
            nombre2 = int(entree_nombre2.get(), 16)
        else:
            raise ValueError("Base invalide.")

        if operation == "+":
            resultat = nombre1 + nombre2
        elif operation == "-":
            resultat = nombre1 - nombre2
        elif operation == "*":
            resultat = nombre1 * nombre2
        elif operation == "/":
            if nombre2 == 0:
                raise ZeroDivisionError("Division par zéro.")
            resultat = nombre1 // nombre2
        else:
            raise ValueError("Opération invalide")

        if base == "2":
            resultat_converti = decToBin(resultat)
        elif base == "10":
            resultat_converti = str(resultat)
        elif base == "16":
            resultat_converti = decToHex(resultat)
        else:
            raise ValueError("Base invalide.")

        label_resultat.config(text=f"Résultat : {resultat_converti}")
    except ValueError:
        messagebox.showerror("Erreur", "Entrée invalide ou opération incorrecte.")
    except ZeroDivisionError as e:
        messagebox.showerror("Erreur", str(e))

def changer_base(*args):
    base = base_selectionnee.get()

    try:
        if base == "2":
            val1 = entree_nombre1.get()
            val2 = entree_nombre2.get()
            if all(c in "01" for c in val1) and all(c in "01" for c in val2):
                entree_nombre1.delete(0, tk.END)
                entree_nombre2.delete(0, tk.END)
                entree_nombre1.insert(0, decToBin(int(val1, 10)))
                entree_nombre2.insert(0, decToBin(int(val2, 10)))
            else:
                raise ValueError("Les nombres ne sont pas valides en base 2.")
        elif base == "10":
            val1 = entree_nombre1.get()
            val2 = entree_nombre2.get()
            if all(c.isdigit() for c in val1) and all(c.isdigit() for c in val2):
                entree_nombre1.delete(0, tk.END)
                entree_nombre2.delete(0, tk.END)
                entree_nombre1.insert(0, str(int(val1, 2)))
                entree_nombre2.insert(0, str(int(val2, 2)))
            else:
                raise ValueError("Les nombres ne sont pas valides en base 10.")
        elif base == "16":
            val1 = entree_nombre1.get()
            val2 = entree_nombre2.get()
            if all(c in "0123456789ABCDEF" for c in val1.upper()) and all(c in "0123456789ABCDEF" for c in val2.upper()):
                entree_nombre1.delete(0, tk.END)
                entree_nombre2.delete(0, tk.END)
                entree_nombre1.insert(0, decToHex(int(val1, 10)))
                entree_nombre2.insert(0, decToHex(int(val2, 10)))
            else:
                raise ValueError("Les nombres ne sont pas valides en base 16.")

        calculer_resultat()

    except ValueError:
        messagebox.showerror("Erreur", "Impossible de convertir les nombres.")

fenetre = tk.Tk()
fenetre.title("Calculatrice de développeur")

label_nombre1 = tk.Label(fenetre, text="Nombre 1 :")
label_nombre1.grid(row=0, column=0, padx=10, pady=10)
entree_nombre1 = tk.Entry(fenetre)
entree_nombre1.grid(row=0, column=1, padx=10, pady=10)

label_nombre2 = tk.Label(fenetre, text="Nombre 2 :")
label_nombre2.grid(row=1, column=0, padx=10, pady=10)
entree_nombre2 = tk.Entry(fenetre)
entree_nombre2.grid(row=1, column=1, padx=10, pady=10)

label_operation = tk.Label(fenetre, text="Opération :")
label_operation.grid(row=2, column=0, padx=10, pady=10)
operation_selectionnee = tk.StringVar(value="+")
menu_operations = ttk.Combobox(fenetre, textvariable=operation_selectionnee, values=["+", "-", "*", "/"], state="readonly")
menu_operations.grid(row=2, column=1, padx=10, pady=10)

label_base = tk.Label(fenetre, text="Base :")
label_base.grid(row=3, column=0, padx=10, pady=10)
base_selectionnee = tk.StringVar(value="10")
menu_bases = ttk.Combobox(fenetre, textvariable=base_selectionnee, values=["2", "10", "16"], state="readonly")
menu_bases.grid(row=3, column=1, padx=10, pady=10)

bouton_calculer = tk.Button(fenetre, text="Calculer", command=calculer_resultat)
bouton_calculer.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

label_resultat = tk.Label(fenetre, text="Résultat :")
label_resultat.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

base_selectionnee.trace_add("write", changer_base)

fenetre.mainloop()
