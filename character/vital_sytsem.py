from dataclasses import dataclass
from .utils import CharacterComponent


@dataclass
class VitalStats:
    level: int = 1
    exp: int = 0
    exp_to_next: int = 100
    max_hp: int = 500
    current_hp: int = 500
    max_mp: int = 50
    current_mp: int = 50


class VitalSystem(CharacterComponent):
    def __init__(self, config: 'CharacterConfig'):
        self.stats = VitalStats()
        self.config = config

    def update(self, character: 'Character') -> None:
        self._calculate_max_hp(character)
        self._calculate_max_mp(character)
        self._apply_limits()

    def _calculate_max_hp(self, character: 'Character') -> None:
        base = self.config.base_hp
        stat_bonus = character.total_stats.stamina * self.config.hp_per_stamina
        equipment_bonus = sum(
            item.bonuses.max_hp
            for item in character.equipment_system.equipment.values()
            if item
        )
        self.stats.max_hp = base + stat_bonus + equipment_bonus

    def _calculate_max_mp(self, character: 'Character') -> None:
        base = self.config.base_mp
        stat_bonus = character.total_stats.intelligence * self.config.mp_per_intelligence
        equipment_bonus = sum(
            item.bonuses.max_mp
            for item in character.equipment_system.equipment.values()
            if item
        )
        self.stats.max_mp = base + stat_bonus + equipment_bonus

    def _apply_limits(self) -> None:
        self.stats.current_hp = min(max(self.stats.current_hp, 0), self.stats.max_hp)
        self.stats.current_mp = min(max(self.stats.current_mp, 0), self.stats.max_mp)

    def take_damage(self, damage: int) -> None:
        self.stats.current_hp = max(self.stats.current_hp - damage, 0)

    def heal(self, amount: int) -> None:
        self.stats.current_hp = min(self.stats.current_hp + amount, self.stats.max_hp)

    def use_mana(self, amount: int) -> None:
        self.stats.current_mp = max(self.stats.current_mp - amount, 0)

    def restore_mana(self, amount: int) -> None:
        self.stats.current_mp = min(self.stats.current_mp + amount, self.stats.max_mp)

    def full_restore(self) -> None:
        self.stats.current_hp = self.stats.max_hp
        self.stats.current_mp = self.stats.max_mp
