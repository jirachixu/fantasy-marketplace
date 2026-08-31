import random
import json

with open("loot/loot_table_weapons.json", "r") as f:
    loot_table_weapons_json = f.read()

loot_table_weapons = json.decoder.JSONDecoder().decode(loot_table_weapons_json)

with open("loot/loot_table_armor.json", "r") as f:
    loot_table_armor_json = f.read()

loot_table_armor = json.decoder.JSONDecoder().decode(loot_table_armor_json)

def get_weighted_choice(weight_dict: dict[str, int]) -> str:
    '''
    Generates a weighted random choice from a dictionary of weights. The keys of the dictionary are the items to choose from, 
    and the values are their corresponding weights. The function returns a randomly chosen item.
    Args:
        weight_dict (dict[str, int]): A dictionary where keys are items and values are their weights.
    Returns:
        str: A randomly chosen item based on the weights provided.
    '''
    return random.choices(
        population=list(weight_dict.keys()), 
        weights=list(weight_dict.values()), 
        k=1
    )[0]