import numpy
import matplotlib.pyplot as plt

table = {}

def importation(fichier: str) -> dict:
    file = open(fichier, "r", encoding="utf8")
    name = fichier.replace(".csv", "")
    descripteurs = file.readline().rstrip().split(";")
    table[name] = {}
    for line in file.readlines():
        values = line.rstrip().split(";")
        table[name][values[0]] = {descripteurs[i].lower(): values[i] for i in range(1, len(descripteurs))}

    file.close()
    return table[name]

cities = importation("cities.csv")
countries = importation("countries.csv")

def afficher(data: dict) -> None:
    for (key, value) in data.items():
        print(f"{key} : {value}")

def affichers(datas: dict) -> None:
    for (key, value) in datas.items():
        afficher(value)
        print()

def recherche(datas: dict, name: str) -> dict:
    for (key, value) in datas.items():
        if key == name or value["name"] == name:
            return value

def nbPopulationFR():
    return nbPopulation("FR")

def nbPopulation(country: str) -> int:
    return int(recherche(countries, country)["population"])

def codesDollar() -> dict:
    codes = {}
    for (key, value) in countries.items():
        if "dollar" in value["currency_name"].lower():
            codes[key] = value
    return codes

def top20paysPopulation() -> list:
    sorted_countries = sorted(countries.items(), key=lambda item: int(item[1]["population"]), reverse=True)
    top_20 = []
    for country, data in sorted_countries[:20]:
        top_20.append((country, data["population"]))
    return top_20

def moyenneHabitantVille() -> dict:
    moyennes = {}
    for country, data in countries.items():
        total_population = 0
        city_count = 0
        for city, city_data in cities.items():
            if city_data["country_iso"] == country:
                total_population += int(city_data["population"])
                city_count += 1
        if city_count > 0:
            moyennes[country] = total_population / city_count
        else:
            moyennes[country] = 0
    return moyennes

def ajouterVille(newCity: dict) -> None:
    city_name = newCity["name"]
    descripteurs = list(next(iter(cities.values())).keys())
    for desc in descripteurs:
        if desc not in newCity:
            newCity[desc] = ""
    cities[city_name] = newCity
    save("cities.csv", cities)

def save(fichier: str, data: dict) -> None:
    with open(fichier, "w", encoding="utf8") as file:
        descripteurs = list(next(iter(data.values())).keys())
        file.write("name;" + ";".join(descripteurs) + "\n")
        for key, value in data.items():
            values = [key] + [value[desc] for desc in descripteurs]
            file.write(";".join(values) + "\n")

def afficher_monde():
    x=[]
    y=[]
    
    for citie in cities.values():
        x.append(float(citie['longitude']))
        y.append(numpy.arcsinh(numpy.tan(float(citie['latitude']) * numpy.pi / 180)))
    plt.scatter(x, y)
    plt.show()

def afficher_carte():
    x=[]
    y=[]
    colors=[]
    
    for citie in cities.values():
        x.append(float(citie['longitude']))
        y.append(numpy.arcsinh(numpy.tan(float(citie['latitude']) * numpy.pi / 180)))
        colors.append(int(citie['population']) / 10000)
    plt.scatter(x, y, s=colors)
    plt.show()

afficher_monde()