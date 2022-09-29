import csv
import ast

def read_csv(filepath):

    list_of_entries = []

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            if "creators" in row.keys():
                row["creators"] = ast.literal_eval(row["creators"])
            
            if "keywords" in row.keys():       
                row["keywords"] = ast.literal_eval(row["keywords"])
            
            if "contributors" in row.keys():
                row["contributors"] = ast.literal_eval(row["contributors"])
            
            if "communities" in row.keys():
                row["communities"] = ast.literal_eval(row["communities"])
            #print(type(row["custom"]))
            if "custom" in row.keys():
                row["custom"] = ast.literal_eval(row["custom"])
            #print(type(row["custom"]))
            #print(row)

            list_of_entries.append(row)

    return list_of_entries


def write_csv(filepath, list_of_records, fieldnames):
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for record in list_of_records:
            writer.writerow(record)


def combine_csv(resulting_file, combining_file):

    combining = []
    resulting = []

    with open(combining_file, 'r', newline='', encoding='utf-8') as comb_file:

        combining_data = csv.DictReader(comb_file)

        for combining_row in combining_data:
            combining.append(combining_row)


    with open(resulting_file, 'r', newline='', encoding='utf-8') as result_file:

        resulting_data = csv.DictReader(result_file)

        for resulting_row in resulting_data:
            resulting.append(resulting_row)

    for result_row in resulting:
        for comb_row in combining:
            if result_row['doi'] == comb_row['doi']:
                result_row['filename'] = comb_row['filename']
                break

    write_csv('projects/covihost/data/combined_csvs.csv', resulting, list(resulting[0].keys()))
