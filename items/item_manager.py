import json
from typing import Dict, Optional, List
from .item import Item, ItemBonuses
from .weapon import Weapon, WeaponBonus
from enums import ItemType, WeaponType, DamageType, ArmorSlot


class ItemManager:
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self.weapons: Dict[str, Weapon] = {}

    def load_from_json(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Хорошо было бы отделить в ItemsProvider, чтобы скрыть детали реализации, что это json-файлы

        for item_data in data.get("items", []):
            self._parse_item(item_data)

    def _parse_item(self, item_data: dict) -> None:
        try:
            item_type = ItemType(item_data["type"].upper())

            if item_type == ItemType.WEAPON:
                self._create_weapon(item_data)
            else:
                self._create_generic_item(item_data)

        except (KeyError, ValueError) as e:
            print(f"Error parsing item {item_data.get('id')}: {str(e)}")

    def _create_weapon(self, data: dict) -> None:
        weapon = Weapon(
            id=data["id"],
            name=data["name"],
            item_type=ItemType.WEAPON,
            slot=ArmorSlot(data["slot"].upper()),
            weapon_type=WeaponType(data["weapon_type"].upper()),
            base_damage=data["base_damage"],
            damage_type=DamageType(data["damage_type"].upper()),
            attack_speed=data["attack_speed"],
            crit_chance=data.get("crit_chance", 0.05),
            stat_scaling=data.get("stat_scaling", {}),
            bonuses=WeaponBonus(**data.get("bonuses", {})),
            description=data.get("description", ""),
            weight=data.get("weight", 0.0),
            value=data.get("value", 0),
            durability=data.get("durability")
        )
        self.items[weapon.id] = weapon
        self.weapons[weapon.id] = weapon

    def _create_generic_item(self, data: dict) -> None:
        item = Item(
            id=data["id"],
            name=data["name"],
            item_type=ItemType(data["type"].upper()),
            slot=ArmorSlot(data["slot"].upper()) if "slot" in data else None,
            bonuses=ItemBonuses(**data.get("bonuses", {})),
            description=data.get("description", ""),
            weight=data.get("weight", 0.0),
            value=data.get("value", 0),
            durability=data.get("durability"),
            effects=data.get("effects", [])
        )
        self.items[item.id] = item

    def get_item(self, item_id: str) -> Optional[Item]:
        return self.items.get(item_id)

    def get_weapon(self, weapon_id: str) -> Optional[Weapon]:
        return self.weapons.get(weapon_id)

    def get_all_items(self) -> List[Item]:
        return list(self.items.values())
