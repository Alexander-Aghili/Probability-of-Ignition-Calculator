from csv_parse import read_table_a
from json_parser import read_json_table
from enum import Enum
import math

class Conditions: 
    dry_bulb_temperature : int = None 
    relative_humidity_percentage : int = None
    direction : str = None 
    slope : str = None 
    shading: str = None 
    time_of_day : int = None 
    altitude_diff : str = None

    def init(self):
        return

    def print(self):
        print("Direction: " + str(self.direction))


def round_down_by_n(number, n):
    return (math.floor(number / n) * n)

def round_down_20(number):
    return math.floor((number - 10) / 20) * 20 + 10


def get_direction():
    return input("What is the direction (N/E/S/W): ").strip()

def get_altitude_diff():
    alt = int(input("What is the altitude difference from wx station (use negative for below): ").strip())
    if alt < -1000:
        return 'B'
    elif alt > 1000:
        return 'A'
    else:
        return 'L'

def get_bool(str_in):
    if (str_in == "y" or str_in == "Y"):
        return True 
    else:
        return False

def is_shaded(val):
    if val == True:
        return "Shaded"
    else:
        return "Unshaded"

def is_sloped(val):
    if val == True:
        return "Slope"
    else:
        return "NoSlope"

def get_conditions():
    conditions = Conditions()
    conditions.dry_bulb_temperature = round_down_by_n(int(input("What is the dry bulb temperate (Integer): ")), 10)
    conditions.relative_humidity_percentage = round_down_by_n(int(input("What is the relative humidity percentage (Integer): ")), 5)
    conditions.direction = get_direction()
    conditions.slope = is_sloped(get_bool(input("Is the shade >50% (y/n): ")))
    conditions.shading = is_shaded(get_bool(input("Is the slope > 30% (y/n): ")))
    conditions.time_of_day = round_down_by_n(int(input("What is time of day (24 hrs use #### format eg. 1800): ")), 200)
    conditions.altitude_diff = get_altitude_diff()
    return conditions

def get_proper_fire_adjustment_data():
    month = int(input("Provide Month (Num only): "))
    if month >= 5 and month <= 7:
        return read_json_table("fire_table_b.json")
    elif month >= 11 or month == 1:
        return read_json_table("fire_table_d.json")
    else:
        return read_json_table("fire_table_c.json")

conditions = get_conditions()
conditions.print()

initial_table = read_table_a()
adjustment_table = get_proper_fire_adjustment_data()
final_table = read_json_table("fire_table_e.json")

def calculate_probability_of_ignition(conditions, initial_table, final_table, adjustment_table):
    num = int(initial_table[str(round_down_20(conditions.dry_bulb_temperature))][str(conditions.relative_humidity_percentage)])
    adjustment_num = None
    print(conditions.time_of_day)
    if conditions.shading == "Shaded": 
        adjustment_num = adjustment_table[conditions.shading][conditions.direction][str(conditions.time_of_day)][conditions.altitude_diff]
    else:
        adjustment_num = adjustment_table[conditions.shading][conditions.direction][conditions.slope][str(conditions.time_of_day)][conditions.altitude_diff]

    num = int(num) + int(adjustment_num)
    return final_table[conditions.shading][str(conditions.dry_bulb_temperature)][str(num)]

probability_of_ignition = calculate_probability_of_ignition(conditions, initial_table, final_table, adjustment_table)
print("\n\n\n\n")
print(probability_of_ignition)