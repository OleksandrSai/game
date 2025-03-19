from dataclasses import asdict, fields
from typing import List, Iterable
import json
from enums import ArmorSlot, CharacterClass, Race, ItemType
from .character_config import CharacterConfig
from .equipment_system import EquipmentSystem
from .base_stat import BaseStats
from items.item import Item
from .level_system import LevelingSystem
from .vital_sytsem import VitalSystem
from .utils import CharacterComponent
from .damage_system import DamageSystem


class Character:
    name: str
    race: Race = Race.HUMAN
    char_class: CharacterClass = CharacterClass.MAGE
    inventory: List[Item] = []
    config: CharacterConfig = CharacterConfig()
    components: List[CharacterComponent] = []

    def __init__(self):
        self.base_stats = BaseStats()
        self.damage_system = DamageSystem(self, self.config)
        self._init_systems()
        self._init_class_stats()

    def _init_systems(self):
        self.vital_system = VitalSystem(self.config)
        self.leveling_system = LevelingSystem(self.config)
        self.equipment_system = EquipmentSystem(self)

    def use_item(self, item_id: str) -> bool:
        item = next((i for i in self.inventory if i.id == item_id), None)
        if item:
            return item.use(self)
        return False

    def _init_class_stats(self):
        class_bonuses = self.config.class_bonuses.get(self.char_class.name, {})
        for stat, value in class_bonuses.items():
            setattr(self.base_stats, stat, getattr(self.base_stats, stat) + value)

    def _get_valid_equipped_items(self) -> Iterable[Item]:
        return (
            item for item in self.equipment_system.equipment.values()
            if item and item.bonuses.stats
        )

    def _apply_stats_bonuses(self, base_stats: BaseStats, bonuses: BaseStats) -> None:
        for field in fields(BaseStats):
            stat_name = field.name
            current_value = getattr(base_stats, stat_name)
            bonus_value = getattr(bonuses, stat_name, 0)
            setattr(base_stats, stat_name, current_value + bonus_value)

    @property
    def attack_damage(self) -> float:
        return self.damage_system.calculate_damage()

    @property
    def total_stats(self) -> BaseStats:
        total = BaseStats(**asdict(self.base_stats))

        equipment_bonuses = self.equipment_system.get_bonuses()

        for stat_field in fields(BaseStats):
            stat_name = stat_field.name
            bonus = equipment_bonuses.get(stat_name, 0)
            setattr(total, stat_name, getattr(total, stat_name) + bonus)

        return total

    def gain_exp(self, amount: int):
        self.leveling_system.gain_exp(self, amount)

    def equip_item(self, item: Item):
        self.equipment_system.equip_item(item)

    def unequip_item(self, slot: ArmorSlot):
        self.equipment_system.unequip_item(slot)

    def save(self, filename: str):
        """Save character to file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @property
    def current_hp(self) -> int:
        return self.vital_system.stats.current_hp

    @property
    def current_mp(self) -> int:
        return self.vital_system.stats.current_mp

    def take_damage(self, damage: int) -> None:
        self.vital_system.take_damage(damage)

    def heal(self, amount: int) -> None:
        self.vital_system.heal(amount)

    def use_mana(self, amount: int) -> None:
        self.vital_system.use_mana(amount)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "race": self.race.name,
            "class": self.char_class.name,
            "base_stats": asdict(self.base_stats),
            "vitals": asdict(self.vital_system.stats),
            "equipment": {
                slot.name: item.id if item else None
                for slot, item in self.equipment_system.equipment.items()
            },
            "inventory": [item.id for item in self.inventory]
        }

    def show_status(self) -> None:
        print(f"\n=== {self.name} ===")
        print(f"Race: {self.race.name}")
        print(f"Class: {self.char_class.name}")
        print(f"Level: {self.vital_system.stats.level}")
        print(f"EXP: {self.vital_system.stats.exp}/{self.vital_system.stats.exp_to_next}")
        print(f"HP: {self.vital_system.stats.current_hp}/{self.vital_system.stats.max_hp}")
        print(f"MP: {self.vital_system.stats.current_mp}/{self.vital_system.stats.max_mp}")

        print("\nAttributes:")
        stats = asdict(self.total_stats)
        for stat, value in stats.items():
            print(f"- {stat.capitalize()}: {value}")

        print("\nEquipment:")
        for slot, item in self.equipment_system.equipment.items():
            item_name = item.name if item else "Empty"
            print(f"{slot.name.capitalize():<10} {item_name}")

        print("\nInventory:")
        for item in self.inventory:
            if item.item_type == ItemType.MONEY:
                print(f"{item.name:<20} x{item.value}")

