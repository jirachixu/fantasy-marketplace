import random
from constants import LOOT_TAGS, ELEMENTAL_TAGS, RUNES
import abc

class Item(abc.ABC):
    def __init__(self, name: str, tags: list[str]):
        self.name = name
        self.tags = tags

    @abc.abstractmethod
    def _calculate_effective_stats(self, base_stats: dict[str, float]) -> dict[str, float]:
        pass

class Rune():
    def __init__(self, rune_name: str, description: str, stat_to_modify: str, multiplier: float, apply_to: str, is_elemental: bool):
        self.rune_name = rune_name
        self.description = description
        self.stat_to_modify = stat_to_modify
        self.multiplier = multiplier
        self.apply_to = apply_to
        self.is_elemental = is_elemental
        self.is_slotted = False

    def __str__(self):
        return f"{self.rune_name}: {self.description} (Modifies {self.stat_to_modify})"

class Weapon(Item):
    def __init__(self, base: str, level: str, prefix: str, suffix: str, base_damage: float, speed: float, range: float, 
        tags: list[tuple[str, str]], damage_type: str
    ):
        self.base = base
        self.level = level
        self.prefix = prefix
        self.suffix = suffix
        self.name = " ".join([part for part in [level, prefix, base, suffix] if part])
        self.damage_type = damage_type
        base_stats = {
            "physical_damage": base_damage if self.damage_type == "physical" else 0,
            "magic_damage": base_damage if self.damage_type == "magical" else 0,
            "fire_damage": 0,
            "ice_damage": 0,
            "lightning_damage": 0,
            "arcane_damage": 0,
            "void_damage": 0,
            "true_damage": 0,
            "speed": speed,
            "range": range,
        }
        self.tags = tags
        self.stats = self._calculate_effective_stats(base_stats)
        self.num_sockets = random.randint(0, 3)
        self.sockets = []

    def _calculate_effective_stats(self, base_stats: dict[str, float]) -> dict[str, float]:
        """
        Calculates the effective stats of the weapon based on its tags and their corresponding multipliers.
        Args:
            base_stats (dict[str, float]): The base stats of the weapon before applying tag multipliers.
        Returns:
            dict[str, float]: The effective stats of the weapon after applying tag multipliers.
        """
        for tag, _ in self.tags:
            if tag in LOOT_TAGS:
                stat_to_modify = LOOT_TAGS[tag]["stat"]
                multiplier = LOOT_TAGS[tag]["multiplier"]
                if stat_to_modify == "damage":
                    if self.damage_type == "physical":
                        base_stats["physical_damage"] *= multiplier
                    elif self.damage_type == "magical":
                        base_stats["magic_damage"] *= multiplier
                elif stat_to_modify in base_stats:
                    base_stats[stat_to_modify] *= multiplier

        damage = max(base_stats["physical_damage"], base_stats["magic_damage"])
        
        for elemental_tag, _ in self.tags:
            if elemental_tag in ELEMENTAL_TAGS:
                elemental_stat = ELEMENTAL_TAGS[elemental_tag]["stat"]
                base_stats[elemental_stat] += damage * ELEMENTAL_TAGS[elemental_tag]["elemental_fraction"]
        return base_stats

    def add_rune(self, rune: Rune):
        """
        Adds a rune to the weapon's sockets if there is an available socket.
        Args:
            rune (Rune): The rune to be added to the weapon.
        """
        if len(self.sockets) >= self.num_sockets or rune.apply_to != "weapon" or rune.is_slotted:
            print(f"Cannot add rune {rune.rune_name}. No available sockets or wrong rune type or already slotted.")
            return
        self.sockets.append(rune)
        rune.is_slotted = True
        if rune.is_elemental:
            self.stats[rune.stat_to_modify] += 4.0
        else:
            self.stats[rune.stat_to_modify] *= rune.multiplier

    def __str__(self):
        tags_str = ', '.join(f"{tag} ({source})" for tag, source in self.tags)
        return f"{self.name} ({', '.join(f'{stat}: {value}' for stat, value in self.stats.items())}, Tags: {tags_str})"

class Armor(Item):
    def __init__(self, base: str, level: str, prefix: str, suffix: str, base_defense: float, movement_speed: float, 
        base_magic_resistance: float, tags: list[tuple[str, str]]
    ):
        self.base = base
        self.level = level
        self.prefix = prefix
        self.suffix = suffix
        self.name = " ".join([part for part in [level, prefix, base, suffix] if part])
        base_stats = {
            "defense": base_defense,
            "magic_resist": base_magic_resistance,
            "movement_speed": movement_speed,
            "fire_resist": 1,
            "ice_resist": 1,
            "lightning_resist": 1,
            "arcane_resist": 1,
            "void_resist": 1,
        }
        self.tags = tags
        self.stats = self._calculate_effective_stats(base_stats)
        self.num_sockets = random.randint(0, 3)
        self.sockets = []

    def _calculate_effective_stats(self, base_stats: dict[str, float]) -> dict[str, float]:
        """
        Calculates the effective stats of the armor based on its tags and their corresponding multipliers.
        Args:
            base_stats (dict[str, float]): The base stats of the armor before applying tag multipliers.
        Returns:
            dict[str, float]: The effective stats of the armor after applying tag multipliers.
        """
        for tag, _ in self.tags:
            if tag in LOOT_TAGS:
                stat_to_modify = LOOT_TAGS[tag]["stat"]
                multiplier = LOOT_TAGS[tag]["multiplier"]
                if stat_to_modify in base_stats:
                    base_stats[stat_to_modify] *= multiplier
        
        for elemental_tag, _ in self.tags:
            if elemental_tag in ELEMENTAL_TAGS:
                elemental_stat = ELEMENTAL_TAGS[elemental_tag]["stat"]
                base_stats[elemental_stat] -= 0.25
        return base_stats
    
    def add_rune(self, rune: Rune):
        """
        Adds a rune to the armor's sockets if there is an available socket.
        Args:
            rune (Rune): The rune to be added to the armor.
        """
        if len(self.sockets) >= self.num_sockets or rune.apply_to != "armor" or rune.is_slotted:
            print(f"Cannot add rune {rune.rune_name}. No available sockets or wrong rune type or already slotted.")
            return
        self.sockets.append(rune)
        rune.is_slotted = True
        if rune.is_elemental:
            self.stats[rune.stat_to_modify] -= 0.25
        else:
            self.stats[rune.stat_to_modify] *= rune.multiplier
    
    def __str__(self):
        tags_str = ', '.join(f"{tag} ({source})" for tag, source in self.tags)
        return f"{self.name} ({', '.join(f'{stat}: {value}' for stat, value in self.stats.items())}, Tags: {tags_str})"