from typing import Dict, List


class CharacterConfig:
    def __init__(
            self,
            base_hp: int,
            base_mp: int,
            hp_per_stamina: float,
            mp_per_intelligence: float,
            base_exp: int,
            exp_multiplier: float,
            level_stat_bonuses: Dict[int, Dict[str, int]],
            class_bonuses: Dict[str, Dict[str, int]],
            base_crit_chance: int = 10,
            crit_multiplier: int = 1
    ):
        self.base_hp = base_hp
        self.base_mp = base_mp
        self.hp_per_stamina = hp_per_stamina
        self.mp_per_intelligence = mp_per_intelligence
        self.base_exp = base_exp
        self.exp_multiplier = exp_multiplier
        self.level_stat_bonuses = level_stat_bonuses
        self.class_bonuses = class_bonuses
        self.crit_multiplier = crit_multiplier
        self.base_crit_chance = base_crit_chance

    def get_level_bonus(self, level: int) -> Dict[str, int]:
        return self.level_stat_bonuses.get(level, {})

    def get_class_bonus(self, char_class: str) -> Dict[str, int]:
        return self.class_bonuses.get(char_class, {})

    def __repr__(self):
        return (f"CharacterConfig(base_hp={self.base_hp}, base_mp={self.base_mp}, "
                f"hp_per_stamina={self.hp_per_stamina}, mp_per_intelligence={self.mp_per_intelligence}, "
                f"base_exp={self.base_exp}, exp_multiplier={self.exp_multiplier}, "
                f"level_stat_bonuses={self.level_stat_bonuses}, class_bonuses={self.class_bonuses})")
