from enum import Enum
import random
from constants import WEAPON_LOOT_TABLE, ARMOR_LOOT_TABLE, RUNES
from item import Weapon, Armor, Item, Rune

class ItemType(Enum):
    WEAPON = "Weapon"
    ARMOR = "Armor"

def generate_items(
    loot_table: dict[str, dict],
    k: int = 1,
    item_type: ItemType = ItemType.WEAPON
) -> list[Weapon | Armor]:
    '''
    Generates items to be used in the game based on the loot tables and their weights.
    Args:
        k (int): The number of items to choose.
    Returns:
        list[Item]: A list of randomly chosen items based on the weights provided.
    '''
    item_categories = loot_table.keys()
    generated_items = []
    
    if len(item_categories) == 0:
        return generated_items
    
    chosen_categories = random.choices(list(item_categories), k=k)
    
    for category in chosen_categories:
        bases = loot_table[category]["bases"]
        levels = loot_table[category]["level"]
        prefixes = loot_table[category]["prefixes"]
        suffixes = loot_table[category]["suffixes"]
        
        if not bases or not levels or not prefixes or not suffixes:
            continue
            
        chosen_base = random.choices(list(bases.keys()), [bases[base]["weight"] for base in bases.keys()])[0]
        chosen_level = random.choices(list(levels.keys()), [levels[level]["weight"] for level in levels.keys()])[0]
        chosen_prefix = random.choices(list(prefixes.keys()), [prefixes[prefix]["weight"] for prefix in prefixes.keys()])[0]
        chosen_suffix = random.choices(list(suffixes.keys()), [suffixes[suffix]["weight"] for suffix in suffixes.keys()])[0]
        
        tags_from_bases = [(tag, "base") for tag in bases[chosen_base]["tags"]]
        base_stats_from_bases = bases[chosen_base]["base_stats"]
        
        tags_from_levels = [(tag, "level") for tag in levels[chosen_level]["tags"]]
        prefix_tags = [(tag, "prefix") for tag in prefixes[chosen_prefix]["tags"]]
        suffix_tags = [(tag, "suffix") for tag in suffixes[chosen_suffix]["tags"]]
        
        tags = tags_from_bases + tags_from_levels + prefix_tags + suffix_tags
        
        if item_type == ItemType.WEAPON:
            generated_items.append(
                Weapon(
                    base=chosen_base,
                    level=chosen_level,
                    prefix=chosen_prefix,
                    suffix=chosen_suffix,
                    base_damage=base_stats_from_bases["damage"],
                    speed=base_stats_from_bases["speed"],
                    range=base_stats_from_bases["range"],
                    tags=tags,
                    damage_type="magical" if category == "Magic" else "physical"
                )
            )
        elif item_type == ItemType.ARMOR:
            generated_items.append(
                Armor(
                    base=chosen_base,
                    level=chosen_level,
                    prefix=chosen_prefix,
                    suffix=chosen_suffix,
                    base_defense=base_stats_from_bases["defense"],
                    movement_speed=base_stats_from_bases["movement_speed"],
                    base_magic_resistance=base_stats_from_bases["magic_resist"],
                    tags=tags
                )
            )
    
    return generated_items

def generate_runes(loot_table: dict[str, dict], k: int = 1) -> list[Rune]:
    '''
    Generates runes to be used in the game based on the rune loot table.
    Args:
        k (int): The number of runes to choose.
    Returns:
        list[Rune]: A list of generated runes.
    '''
    runes = []
    for _ in range(k):
        chosen_rune = random.choice(list(loot_table.keys()))
        rune_data = loot_table[chosen_rune]
        stat_to_modify, multiplier = next(iter(rune_data["effect"].items()))
        runes.append(
            Rune(
                rune_name=rune_data["rune_name"],
                description=rune_data["description"],
                stat_to_modify=stat_to_modify,
                multiplier=multiplier,
                apply_to=rune_data["apply_to"],
                is_elemental=rune_data["is_elemental"]
            )
        )
    return runes

def main():
    loot_table = WEAPON_LOOT_TABLE
    item_categories = loot_table.keys()
    
    category = random.choices(list(item_categories), k=1)[0]
    bases = loot_table[category]["bases"]
    chosen_base = random.choices(list(bases.keys()), [bases[base]["weight"] for base in bases.keys()])[0]
    base_stats_from_bases = bases[chosen_base]["base_stats"]
    tags_from_bases = [(tag, "base") for tag in bases[chosen_base]["tags"]]
    print(tags_from_bases)

if __name__ == "__main__":
    main()