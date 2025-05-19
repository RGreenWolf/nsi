t_moy = [14.9, 13.3, 13.1, 12.5, 13.0, 13.6, 13.7]

annees = [2013, 2014, 2015, 2016, 2017, 2018, 2019]

def annee_temperature_minimale(t_moy: list, annees: list) -> tuple:
    min_temp = t_moy[0]
    index = 0
    for i in range(1, len(t_moy)):
        if t_moy[i] < min_temp:
            min_temp = t_moy[i]
            index = i
    return (min_temp, annees[index])

print(annee_temperature_minimale(t_moy, annees))

