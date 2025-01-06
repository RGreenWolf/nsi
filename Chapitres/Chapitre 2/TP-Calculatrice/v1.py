# Dictionnaire pour la conversion hexadécimale
hexToBinDict = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111"
}

# Conversion binaire -> décimal
def binToDec(nombre_bin):
    return sum(int(bit) * (2 ** i) for i, bit in enumerate(nombre_bin[::-1]))

# Conversion décimal -> binaire
def decToBin(nombre_dec):
    if nombre_dec == 0:
        return "0"
    resultat = ""
    while nombre_dec > 0:
        resultat = str(nombre_dec % 2) + resultat
        nombre_dec //= 2
    return resultat

# Conversion décimal -> hexadécimal
def decToHex(nombre_dec):
    if nombre_dec == 0:
        return "0"
    resultat = ""
    while nombre_dec > 0:
        reste = nombre_dec % 16
        resultat = (chr(55 + reste) if reste >= 10 else str(reste)) + resultat
        nombre_dec //= 16
    return resultat

# Conversion binaire -> hexadécimal
def binToHex(nombre_bin):
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
    hex_to_dec_dict = {k: int(k, 16) for k in hexToBinDict.keys()}
    return sum(hex_to_dec_dict[char] * (16 ** i) for i, char in enumerate(nb_hex[::-1]))

# Conversion décimal négatif -> binaire (complément à 2)
def decNegToBin(nb_neg_dec):
    if nb_neg_dec >= 0:
        raise ValueError("Le nombre doit être négatif.")
    nb_complement_2 = (1 << 8) + nb_neg_dec
    return decToBin(nb_complement_2).zfill(8)

# Conversion binaire négatif -> décimal
def binNegToDec(nb_neg_bin):
    if nb_neg_bin[0] == "1":
        return binToDec(nb_neg_bin) - (1 << len(nb_neg_bin))
    return binToDec(nb_neg_bin)

def decReelToBin(nb_reel_dec, precision=16):
    partie_entiere = int(nb_reel_dec)
    partie_decimale = nb_reel_dec - partie_entiere

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

# Conversion binaire réel -> décimal
def binReelToDec(nb_reel_bin):
    partie_entiere, _, partie_decimale = nb_reel_bin.partition(".")
    dec_entiere = binToDec(partie_entiere)
    dec_decimale = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(partie_decimale))
    return dec_entiere + dec_decimale

# Tests
nb_bin_in = "101000010010"
nb_dec_in = 2578
nb_hex_in = "A12"

assert binToDec(nb_bin_in) == 2578, "Houston we've got a problem!"
assert decToBin(nb_dec_in) == "101000010010", "Houston we've got a problem!"
assert decToHex(nb_dec_in) == "A12", "Houston we've got a problem!"
assert binToHex(nb_bin_in) == "A12", "Houston we've got a problem!"
assert hexToBin(nb_hex_in) == "101000010010", "Houston we've got a problem!"
assert hexToDec(nb_hex_in) == 2578, "Houston we've got a problem!"
assert decNegToBin(-66) == "10111110", "Houston we've got a problem!"
assert binNegToDec("11011111") == -33, "Houston we've got a problem!"
assert decReelToBin(3.5) == "11.100000000000000", "Houston we've got a problem!"
assert binReelToDec("11.100000000000000") == 3.5, "Houston we've got a problem!"
