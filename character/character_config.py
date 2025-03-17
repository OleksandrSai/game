from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CharacterConfig:
    base_hp: int = field(default=500)
    base_mp: int = field(default=300)
    hp_per_stamina: int = field(default=5)
    mp_per_intelligence: int = field(default=3)
    base_exp: int = field(default=0)
    exp_multiplier: float = field(default=1)
    class_bonuses: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        "warrior": {
            "strength": 5,
            "stamina": 3
        },
        "mage": {
            "intelligence": 7,
            "dexterity": 2
        },
        "archer": {
            "dexterity": 6,
            "luck": 2
        }
    })


character_config = CharacterConfig()
