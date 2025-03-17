from typing import Dict, Optional, List, Union
from enums import ArmorSlot, ItemType
from items.item import Item


class EquipmentSystem:
    def __init__(self, character: 'Character'):
        self.character = character
        self.equipment: Dict[ArmorSlot, Optional[Item]] = {
            slot: None for slot in ArmorSlot
        }

    def equip_item(self, item: Item) -> bool:
        if item.slot is None:
            return False

        if self.equipment[item.slot]:
            self.unequip_item(item.slot)

        self.equipment[item.slot] = item
        self.character.inventory.remove(item)
        return True

    def unequip_item(self, slot: ArmorSlot) -> Optional[Item]:
        if item := self.equipment.get(slot):
            self.character.inventory.append(item)
            self.equipment[slot] = None
            return item
        return None

    def _validate_item(self, item: Item) -> bool:
        return all([
            item.slot is not None,
            self._check_item_type(item)
        ])

    def _check_item_type(self, item: Item) -> bool:
        type_to_slot_mapping = {
            ItemType.WEAPON: [ArmorSlot.WEAPON],
            ItemType.ARMOR: [
                ArmorSlot.HELMET,
                ArmorSlot.CHEST,
                ArmorSlot.GLOVES,
                ArmorSlot.PANTS,
                ArmorSlot.BOOTS
            ]
        }
        return item.slot in type_to_slot_mapping.get(item.item_type, [])

    def get_equipped_items(self) -> List[Item]:
        return [item for item in self.equipment.values() if item]

    def get_bonuses(self) -> Dict[str, Union[int, float]]:
        """Возвращает суммарные бонусы от всей экипировки."""
        bonuses = {}
        for item in self.get_equipped_items():
            if not item.bonuses:
                continue

            if item.bonuses.damage > 0:
                bonuses["damage"] = bonuses.get("damage", 0) + item.bonuses.damage

            if item.bonuses.critical_chance > 0:
                bonuses["critical_chance"] = round(bonuses.get("critical_chance", 0.0) + item.bonuses.critical_chance, 2)

        return bonuses
