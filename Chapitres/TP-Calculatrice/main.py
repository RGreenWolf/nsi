# Fonction : Base 2 -> Base 10
def binToDec(nb_bin):
    result = 0
    power = 0
    for digit in reversed(nb_bin):
        result += int(digit) * (2 ** power)
        power += 1
    return result

# Fonction : Base 10 -> Base 2
def decToBin(nb_dec):
    result = ""
    while nb_dec > 0:
        result = str(nb_dec % 2) + result
        nb_dec //= 2
    return result if result else "0"

# Fonction : Base 2 -> Base 16
def binToHex(nb_bin):
    decimal = binToDec(nb_bin)
    return decToHex(decimal)

# Fonction : Base 16 -> Base 2
def hexToBin(nb_hex):
    decimal = hexToDec(nb_hex)
    return decToBin(decimal)

# Fonction : Base 10 -> Base 16
def decToHex(nb_dec):
    hex_chars = "0123456789ABCDEF"
    result = ""
    while nb_dec > 0:
        result = hex_chars[nb_dec % 16] + result
        nb_dec //= 16
    return result if result else "0"

# Fonction : Base 16 -> Base 10
def hexToDec(nb_hex):
    hex_chars = "0123456789ABCDEF"
    result = 0
    power = 0
    for digit in reversed(nb_hex):
        result += hex_chars.index(digit.upper()) * (16 ** power)
        power += 1
    return result

# Fonction : Base 10 négative -> Base 2 (complément à 2)
def decNegToBin(nb_neg_dec, length=8):
    if nb_neg_dec >= 0:
        raise ValueError("Le nombre doit être négatif.")
    
    # On prend la valeur absolue pour la conversion
    nb_pos_dec = abs(nb_neg_dec)
    bin_pos = decToBin(nb_pos_dec)
    
    # Compléter à la longueur souhaitée
    bin_pos = bin_pos.zfill(length)
    
    # Complément à 1 : inverser les bits
    complement = ''.join('1' if bit == '0' else '0' for bit in bin_pos)
    
    # Ajouter 1 au complément (complément à 2)
    carry = 1
    result = ''
    for bit in reversed(complement):
        sum_bit = int(bit) + carry
        result = str(sum_bit % 2) + result
        carry = sum_bit // 2
    
    # Si carry est encore 1, on ajoute le 1 à la fin
    if carry:
        result = '1' + result
    
    # Retourner le résultat
    return result

# Fonction : Base 2 signé -> Base 10 négatif
def binNegToDec(nb_neg_bin):
    if nb_neg_bin[0] == "0":
        return binToDec(nb_neg_bin)
    length = len(nb_neg_bin)
    complement = ""
    for bit in nb_neg_bin:
        complement += "1" if bit == "0" else "0"
    complement = binToDec(complement) + 1
    return -complement

# Fonction : Base 10 réel -> Base 2 réel
def decReelToBin(nb_reel_dec, precision=16):
    entier = int(nb_reel_dec)
    fractionnaire = nb_reel_dec - entier
    entier_bin = decToBin(entier)
    fraction_bin = ""
    
    # Convertir la partie fractionnaire en binaire avec une précision de 'precision' bits
    while fractionnaire and len(fraction_bin) < precision:
        fractionnaire *= 2
        bit = int(fractionnaire)
        fraction_bin += str(bit)
        fractionnaire -= bit

    # Retourner la partie entière et la partie fractionnaire séparées par une virgule
    return entier_bin + "," + fraction_bin if fraction_bin else entier_bin + ",0"

# Fonction : Base 2 réel -> Base 10 réel
def binReelToDec(nb_reel_bin):
    entier_bin, fraction_bin = nb_reel_bin.split(",")
    entier = binToDec(entier_bin)
    fractionnaire = 0
    for i, bit in enumerate(fraction_bin):
        fractionnaire += int(bit) / (2 ** (i + 1))
    return entier + fractionnaire

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
assert decReelToBin(3.5) == "11,100000000000000", "Houston we've got a problem!"
assert binReelToDec("11,100000000000000") == 3.5, "Houston we've got a problem!"
