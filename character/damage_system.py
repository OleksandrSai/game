from typing import Optional
from enums import DamageType
from typing import Dict
from items.weapon import Weapon
import random


class DamageSystem:
    def __init__(self, character, config):
        self.character = character
        self.config = config
        print("===============")
        "CONFIG"
        print("===============")
    def calculate_damage(self, target_resistances: Dict[DamageType, float] = None) -> float:
        weapon = self._get_equipped_weapon()

        base_damage = self._get_base_damage(weapon)

        stat_bonus = self._calculate_stat_bonus(weapon)

        crit_multiplier = self._get_crit_multiplier(weapon)

        total_damage = (base_damage + stat_bonus) * crit_multiplier

        if target_resistances:
            total_damage = self._apply_resistances(
                total_damage,
                weapon.damage_type,
                target_resistances
            )

        return max(0, total_damage)

    def _get_equipped_weapon(self) -> Optional[Weapon]:
        return self.character.equipment_system.get_equipped_items()

    def _get_base_damage(self, weapon: Optional[Weapon]) -> float:
        if weapon:
            weapon = first_weapon = next(iter(weapon), None)
            return weapon.base_damage * weapon.attack_speed
        print(f"{self.config=}")
        return self.config.base_unarmed_damage * self.character.total_stats.strength

    def _calculate_stat_bonus(self, weapon: Optional[list[Weapon]]) -> float:
        first_weapon = next(iter(weapon), None)
        if not first_weapon:
            return self.character.total_stats.strength * self.config.unarmed_stat_multiplier

        bonus = 0
        for stat, multiplier in first_weapon.stat_scaling.items():
            stat_value = getattr(self.character.total_stats, stat, 0)
            bonus += stat_value * multiplier

        return bonus

    def _get_crit_multiplier(self, weapon: Optional[Weapon]) -> float:
        weapon = next(iter(weapon), None)
        weapon_crit = weapon.crit_chance if weapon else 0
        total_crit = 5 + weapon_crit

        if random.random() < total_crit:
            return self.config.exp_multiplier
        return 1.0

    def _apply_resistances(self, damage: float,
                           damage_type: DamageType,
                           resistances: Dict[DamageType, float]) -> float:

        resistance = resistances.get(damage_type, 0)
        return damage * (1 - resistance)
