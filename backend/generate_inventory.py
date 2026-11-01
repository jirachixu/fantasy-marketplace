import random
from constants import WEAPON_LOOT_TABLE, ARMOR_LOOT_TABLE
from item import Weapon, Armor, Item

def get_weighted_choices(weight_dict: dict[Item, int], k: int = 1) -> list[Item]:
    '''
    Generates a weighted random choice from a dictionary of weights. The keys of the dictionary are the items to choose from, 
    and the values are their corresponding weights. The function returns a randomly chosen item.
    Args:
        weight_dict (dict[Item, int]): A dictionary where keys are items and values are their weights.
        k (int): The number of items to choose.
    Returns:
        list[Item]: A list of randomly chosen items based on the weights provided.
    '''
    return random.choices(
        population=list(weight_dict.keys()), 
        weights=list(weight_dict.values()), 
        k=k
    )
    
def main():
    return

if __name__ == "__main__":
    main()