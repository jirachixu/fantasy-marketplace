from constants import LOOT_TAGS, ELEMENTAL_TAGS
import abc

class Item(abc.ABC):
    def __init__(self, name: str, tags: list[str]):
        self.name = name
        self.tags = tags

    @abc.abstractmethod
    def _calculate_effective_stats(self, base_stats: dict[str, float]) -> dict[str, float]:
        pass

class Weapon(Item):
    def __init__(self, name: str, base_damage: float, speed: float, range: float, tags: list[str], damage_type: str):
        self.name = name
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

    def _calculate_effective_stats(self, base_stats: dict[str, float]) -> dict[str, float]:
        """
        Calculates the effective stats of the weapon based on its tags and their corresponding multipliers.
        Args:
            base_stats (dict[str, float]): The base stats of the weapon before applying tag multipliers.
        Returns:
            dict[str, float]: The effective stats of the weapon after applying tag multipliers.
        """
        for tag in self.tags:
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
        
        for elemental_tag in self.tags:
            if elemental_tag in ELEMENTAL_TAGS:
                elemental_stat = ELEMENTAL_TAGS[elemental_tag]["stat"]
                base_stats[elemental_stat] += damage * ELEMENTAL_TAGS[elemental_tag]["elemental_fraction"]
        return base_stats

    def __str__(self):
        primary_damage = max(self.stats["physical_damage"], self.stats["magic_damage"])
        return f"{self.name} ({', '.join(f'{stat}: {value}' for stat, value in self.stats.items())}, Tags: {', '.join(self.tags)})"

class Armor(Item):
    def __init__(self, name: str, base_defense: float, movement_speed: float, base_magic_resistance: float, tags: list[str]):
        self.name = name
        base_stats = {
            "physical_defense": base_defense,
            "magic_resistance": base_magic_resistance,
            "movement_speed": movement_speed,
            "fire_multiplier": 1,
            "ice_multiplier": 1,
            "lightning_multiplier": 1,
            "arcane_multiplier": 1,
            "void_multiplier": 1,
        }
        self.tags = tags
        self.stats = self._calculate_effective_stats(base_stats)

    def _calculate_effective_stats(self, base_stats: dict[str, float]) -> dict[str, float]:
        """
        Calculates the effective stats of the armor based on its tags and their corresponding multipliers.
        Args:
            base_stats (dict[str, float]): The base stats of the armor before applying tag multipliers.
        Returns:
            dict[str, float]: The effective stats of the armor after applying tag multipliers.
        """
        for tag in self.tags:
            if tag in LOOT_TAGS:
                stat_to_modify = LOOT_TAGS[tag]["stat"]
                multiplier = LOOT_TAGS[tag]["multiplier"]
                if stat_to_modify in base_stats:
                    base_stats[stat_to_modify] *= multiplier
        
        for elemental_tag in self.tags:
            if elemental_tag in ELEMENTAL_TAGS:
                elemental_stat = ELEMENTAL_TAGS[elemental_tag]["stat"]
                base_stats[elemental_stat] -= 0.5
        return base_stats
    
    def __str__(self):
        return f"{self.name} ({', '.join(f'{stat}: {value}' for stat, value in self.stats.items())}, Tags: {', '.join(self.tags)})"