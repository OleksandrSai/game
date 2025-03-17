
from .utils import CharacterComponent


class LevelingSystem(CharacterComponent):

    def __init__(self, config: 'CharacterConfig'):
        self.config = config

    def gain_exp(self, character: 'Character', amount: int):
        character.vital_system.stats.exp += amount
        while self._can_level_up(character):
            self._perform_level_up(character)

    def _can_level_up(self, character: 'Character') -> bool:
        return character.vital_system.stats.exp >= character.vital_system.stats.exp_to_next

    def _perform_level_up(self, character: 'Character'):
        character.vital_system.stats.level += 1
        character.vital_system.stats.exp -= character.vital_system.stats.exp_to_next
        self._update_exp_threshold(character)
        self._apply_stat_bonuses(character)
        character.vital_system.update(character)

    def _update_exp_threshold(self, character: 'Character'):
        character.vital_system.stats.exp_to_next = int(
            character.vital_system.stats.exp_to_next * self.config.exp_multiplier
        )

    def _apply_stat_bonuses(self, character: 'Character'):
        for stat, value in self.config.level_stat_bonuses.items():
            setattr(character.base_stats, stat, getattr(character.base_stats, stat) + value)