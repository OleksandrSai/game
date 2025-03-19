from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enums import ItemType, ArmorSlot
from character.base_stat import BaseStats


@dataclass
class ItemBonuses:
    stats: BaseStats = field(default_factory=BaseStats)
    max_hp: int = 0
    max_mp: int = 0


@dataclass
class Item:
    id: str
    name: str
    item_type: ItemType
    description: str = ""
    weight: float = 0.0
    value: int = 0
    stackable: bool = False
    max_stack: int = 1
    slot: Optional[ArmorSlot] = None
    requirements: Dict[str, int] = field(default_factory=dict)
    bonuses: ItemBonuses = field(default_factory=ItemBonuses)
    effects: List[str] = field(default_factory=list)
    durability: Optional[int] = None
    custom_data: Dict = field(default_factory=dict)

    def use(self, character: 'Character') -> bool:
        if self.item_type == ItemType.CONSUMABLE:
            return self._apply_consumable_effects(character)
        return False

    def _apply_consumable_effects(self, character: 'Character') -> bool:
        for effect in self.effects:
            if effect.startswith("heal:"):
                amount = int(effect.split(":")[1])
                character.vital_system.heal(amount)
            elif effect.startswith("mana:"):
                amount = int(effect.split(":")[1])
                character.vital_system.restore_mana(amount)
        return True


def add_money_to_inventory(controller, money_reward):
    money_item = Item(
        id="money_001",
        name="Золотые монеты",
        item_type=ItemType.MONEY,
        description="Монеты, используемые для обмена и покупки товаров.",
        weight=0.01,
        value=money_reward,  # Устанавливаем количество монет, переданное извне
        stackable=True,
        max_stack=10000,
    )
    controller.char.inventory.append(money_item)
