import csv

# Reading CSV file
with open('fire_table_a.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    data = {row[0]: {header[i]: row[i] for i in range(1, len(header))} for row in csv_reader}

# Accessing data
print(data['109+']['15-19'])  # Output: Data1

print(data)
