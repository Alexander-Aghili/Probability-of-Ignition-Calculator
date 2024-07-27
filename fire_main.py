from csv_parse import read_table_a
from json_parser import read_json_table

data_a = read_table_a()
data_b = read_json_table("fire_table_b.json")
print(data_b)