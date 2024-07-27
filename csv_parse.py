import csv

def read_table_a():
    data = None
    with open("fire_table_a.csv", mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = {row[0]: {header[i]: row[i] for i in range(1, len(header))} for row in csv_reader}

    return data
