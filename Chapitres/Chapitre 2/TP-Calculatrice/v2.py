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

# Conversion binaire réel -> décimal
def binReelToDec(nb_reel_bin):
    partie_entiere, _, partie_decimale = nb_reel_bin.partition(".")
    dec_entiere = binToDec(partie_entiere)
    dec_decimale = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(partie_decimale))
    return dec_entiere + dec_decimale

# Conversion décimal réel -> binaire avec précision
def decReelToBin(nb_reel_dec, precision=16):
    partie_entiere = int(nb_reel_dec)
    partie_decimale = abs(nb_reel_dec - partie_entiere)

    bin_entiere = decToBin(partie_entiere)
    bin_decimale = ""
    count = 0
    while partie_decimale > 0 and count < precision:
        partie_decimale *= 2
        bit = int(partie_decimale)
        bin_decimale += str(bit)
        partie_decimale -= bit
        count += 1

    bin_decimale = bin_decimale.ljust(precision - 1, '0')
    return bin_entiere + "." + bin_decimale if bin_decimale else bin_entiere

