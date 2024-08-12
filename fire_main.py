import time
from csv_parse import read_table_a
from json_parser import read_json_table
from enum import Enum
import math

class Conditions: 
    def __init__(self):
        self.dry_bulb_temperature: int = None
        self.relative_humidity_percentage: int = None
        self.direction: str = None
        self.slope: str = None
        self.shading: str = None
        self.time_of_day: int = None
        self.altitude_diff: str = None

    def print(self):
        print(f"Direction: {self.direction}")
        print(f"Dry Bulb Temperature: {self.dry_bulb_temperature}")
        print(f"Relative Humidity: {self.relative_humidity_percentage}")
        print(f"Slope: {self.slope}")
        print(f"Shading: {self.shading}")
        print(f"Time of Day: {self.time_of_day}")
        print(f"Altitude Difference: {self.altitude_diff}")

def round_down_by_n(number: int, n: int) -> int:
    return (math.floor(number / n) * n)

def round_down_20(number: int) -> int:
    return math.floor((number - 10) / 20) * 20 + 10

def get_direction() -> str:
    return input("What is the direction (N/E/S/W): ").strip()

def get_altitude_diff() -> str:
    alt = int(input("What is the altitude difference from wx station (use negative for below): ").strip())
    if alt < -1000:
        return 'B'
    elif alt > 1000:
        return 'A'
    else:
        return 'L'

def get_bool(str_in: str) -> bool:
    return str_in.lower() == "y"

def is_shaded(val: bool) -> str:
    return "Shaded" if val else "Unshaded"

def is_sloped(val: bool) -> str:
    return "Slope" if val else "NoSlope"

def get_time(time):
    if time < 800:
        return 800
    elif time > 1800:
        return 1800
    else:
        return time

def get_conditions() -> Conditions:
    conditions = Conditions()
    conditions.dry_bulb_temperature = round_down_by_n(int(input("What is the dry bulb temperature (Integer): ")), 10)
    conditions.relative_humidity_percentage = round_down_by_n(int(input("What is the relative humidity percentage (Integer): ")), 5)
    conditions.direction = get_direction()
    conditions.slope = is_sloped(get_bool(input("Is the slope > 30% (y/n): ")))
    conditions.shading = is_shaded(get_bool(input("Is the shade >50% (y/n): ")))

    # Automatically get current time and round it
    current_time = time.localtime()
    hour_min = current_time.tm_hour * 100 + current_time.tm_min
    conditions.time_of_day = get_time(round_down_by_n(hour_min, 200))
    
    conditions.altitude_diff = get_altitude_diff()
    return conditions

def get_proper_fire_adjustment_data() -> dict:
    # Automatically get the current month
    current_month = time.localtime().tm_mon
    if 5 <= current_month <= 7:
        return read_json_table("fire_table_b.json")
    elif current_month >= 11 or current_month == 1:
        return read_json_table("fire_table_d.json")
    else:
        return read_json_table("fire_table_c.json")

conditions = get_conditions()
conditions.print()

initial_table = read_table_a()
adjustment_table = get_proper_fire_adjustment_data()
final_table = read_json_table("fire_table_e.json")

def calculate_probability_of_ignition(conditions: Conditions, initial_table: dict, final_table: dict, adjustment_table: dict) -> str:
    num = int(initial_table[str(round_down_20(conditions.dry_bulb_temperature))][str(conditions.relative_humidity_percentage)])
    adjustment_num = None
    
    if conditions.shading == "Shaded": 
        adjustment_num = adjustment_table[conditions.shading][conditions.direction][str(conditions.time_of_day)][conditions.altitude_diff]
    else:
        adjustment_num = adjustment_table[conditions.shading][conditions.direction][conditions.slope][str(conditions.time_of_day)][conditions.altitude_diff]

    num = int(num) + int(adjustment_num)
    return final_table[conditions.shading][str(conditions.dry_bulb_temperature)][str(num)]

probability_of_ignition = calculate_probability_of_ignition(conditions, initial_table, final_table, adjustment_table)
print("\n\n\n\n")
print(probability_of_ignition)
