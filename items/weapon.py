from dataclasses import dataclass, field
from typing import Dict, List
from enums import WeaponType, DamageType, ItemType, ArmorSlot
from .item import Item
import json


@dataclass
class WeaponBonus:
    stats: Dict[str, int] = field(default_factory=dict)
    damage: int = 0
    critical_chance: float = 0.0


@dataclass
class Weapon(Item):
    weapon_type: WeaponType = WeaponType.SWORD
    base_damage: float = 10.0
    damage_type: DamageType = DamageType.PHYSICAL
    attack_speed: float = 1.0
    crit_chance: float = 0.05
    stat_scaling: Dict[str, float] = None
    bonuses: WeaponBonus = field(default_factory=WeaponBonus)


class WeaponLoader:
    @staticmethod
    def load_from_config(file_path: str) -> List[Weapon]:
        with open(file_path, 'r') as f:
            config = json.load(f)
        # WeaponProvider

        weapons = []
        for weapon_data in config.get("weapons", []):
            try:
                weapons.append(WeaponLoader._parse_weapon(weapon_data))
            except (KeyError, ValueError) as e:
                print(f"Error parsing weapon {weapon_data.get('id')}: {str(e)}")

        return weapons

    @staticmethod
    def _parse_weapon(data: dict) -> Weapon:
        item_type = ItemType[data["item_type"].upper()]
        slot = ArmorSlot[data["slot"].upper()] if "slot" in data else None
        weapon_type = WeaponType[data["weapon_type"].upper()]
        damage_type = DamageType[data["damage_type"].upper()]

        bonuses_data = data.get("bonuses", {})
        bonuses = WeaponBonus(
            stats=bonuses_data.get("stats", {}),
            critical_chance=bonuses_data.get("critical_chance", 0.0)
        )

        return Weapon(
            id=data["id"],
            name=data["name"],
            item_type=item_type,
            slot=slot,
            weapon_type=weapon_type,
            base_damage=data["base_damage"],
            damage_type=damage_type,
            attack_speed=data["attack_speed"],
            crit_chance=data.get("crit_chance", 0.05),
            stat_scaling=data.get("stat_scaling", {}),
            bonuses=bonuses,
            description=data.get("description", ""),
            weight=data.get("weight", 0.0),
            value=data.get("value", 0),
            durability=data.get("durability")
        )

