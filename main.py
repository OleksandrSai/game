from game_state import AuthState
from settings.game_config_manager import GameConfigManager
from enums import LoadSource
from config import settings


class GameController:
    def __init__(self, config):
        self.config = config
        self._state = None
        self.user = None
        self.character = None

    def set_user(self, username):
        self.user = username

    def set_character(self, character):
        self.character = character

    def change_state(self, state):
        self._state = state
        if self._state:
            self._state.handle(self)

    def exit(self):
        print("Игра завершена")


if __name__ == '__main__':
    game_config = GameConfigManager.load_character_config(LoadSource.LOCAL, f"{settings.SOURCE_LOAD_PATH}base_config.json")
    controller = GameController(config=game_config)
    controller.change_state(AuthState())
