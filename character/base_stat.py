from dataclasses import dataclass
from typing import Dict


@dataclass
class BaseStats:
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    stamina: int = 10
    luck: int = 5

    def apply_bonuses(self, bonuses: Dict[str, int]) -> None:
        for stat, value in bonuses.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + value)
