import json

def read_json_table(filename):
    data = None
    with open(filename, mode='r') as file:
        data = json.load(file)
    return data

