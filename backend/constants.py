import json
from pathlib import Path

# Resolve path relative to this file so imports work from any working directory
LOOT_DIR = Path(__file__).parent / "loot"

def _load_json(filename: str) -> dict:
    with open(LOOT_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Module-level constants, loaded once into memory on first import
LOOT_TAGS: dict[str, dict] = _load_json("loot_tags.json")
ELEMENTAL_TAGS: dict[str, dict] = _load_json("loot_elemental_tags.json")
WEAPON_LOOT_TABLE: dict[str, dict] = _load_json("loot_table_weapons.json")
ARMOR_LOOT_TABLE: dict[str, dict] = _load_json("loot_table_armor.json")
