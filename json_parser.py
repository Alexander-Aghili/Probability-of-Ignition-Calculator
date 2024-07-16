import json

# Reading JSON file
with open('fire_table_b.json', mode='r') as file:
    data = json.load(file)

print(data['TableB']['Unshaded']['W']['NoSlope']['1000']['A'])
