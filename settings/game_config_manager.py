from enums import LoadSource
from .factory import ConfigLoaderFactory
from .config import CharacterConfig


class GameConfigManager:
    @staticmethod
    def load_character_config(source: LoadSource, location: str) -> 'CharacterConfig':
        loader = ConfigLoaderFactory.create_loader(source, location)
        config_data = loader.load()

        return CharacterConfig(
            base_hp=config_data['base']['hp'],
            base_mp=config_data['base']['mp'],
            hp_per_stamina=config_data['base']['hp_per_stamina'],
            mp_per_intelligence=config_data['base']['mp_per_intelligence'],
            base_exp=config_data['experience']['base_exp'],
            exp_multiplier=config_data['experience']['multiplier'],
            level_stat_bonuses=config_data['experience']['level_stat_bonuses'],
            class_bonuses=config_data['class_bonuses'],
        )

    @staticmethod
    def load_location(source: LoadSource, location: str):
        loader = ConfigLoaderFactory.create_loader(source, location)
        location = loader.load()
        return location
