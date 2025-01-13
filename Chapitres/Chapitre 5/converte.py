import csv

def convert_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['ID', 'name', 'latitude', 'longitude', 'country_iso', 'population', 'identifiant']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        
        writer.writeheader()
        for row in reader:
            new_row = {
                'ID': f"{row['iso3']}-{row['city'].replace(' ', '_')}",
                'name': row['city'],
                'latitude': row['lat'],
                'longitude': row['lng'],
                'country_iso': row['iso3'],
                'population': row['population'],
                'identifiant': row['id']
            }
            writer.writerow(new_row)

convert_csv('worldcities.csv', 'cities.csv')
