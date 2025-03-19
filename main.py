from game_state import AuthState
from settings.game_config_manager import GameConfigManager
from enums import TypeReward, LoadSource
from config import settings
from reward import ExperienceRewardHandler, MoneyRewardHandler


class GameController:
    def __init__(self, config, location):
        self.config = config
        self.location = location
        self.user = None
        self.character = None
        self._state = None
        self.reward_handler_chain = self.create_reward_handler_chain()

    def set_user(self, username):
        self.user = username

    def set_character(self, character):
        self.character = character

    def change_state(self, state):
        self._state = state
        self._state.handle(self)

    def exit(self):
        print("Игра завершена")

    def create_reward_handler_chain(self):
        money_handler = MoneyRewardHandler()
        experience_handler = ExperienceRewardHandler()
        money_handler.set_next(experience_handler)
        return money_handler

    def handle_reward(self, reward_type, amount):
        self.reward_handler_chain.handle_reward(reward_type, amount)


def initialize_game():
    game_config = GameConfigManager.load_character_config(LoadSource.LOCAL,
                                                          f"{settings.SOURCE_LOAD_PATH}base_config.json")
    location = GameConfigManager.load_location(LoadSource.LOCAL, f"{settings.SOURCE_LOAD_PATH}location.json")
    controller = GameController(config=game_config, location=location)
    controller.change_state(AuthState())
    return controller


if __name__ == '__main__':
    controller = initialize_game()
