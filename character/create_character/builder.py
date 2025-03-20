from ..character import Character
from enums import Race, CharacterClass
from items.weapon import Weapon


class CharacterBuilder:
    def __init__(self):
        self.character = Character()
        self.character.inventory = []

    def set_name(self, name: str):
        self.character.name = name
        return self

    def set_race(self, race: Race):
        self.character.race = race
        return self

    def set_class(self, char_class: CharacterClass):
        self.character.char_class = char_class
        return self

    def add_weapon(self, weapon: Weapon):
        self.character.inventory.append(weapon)
        self.character.equip_item(weapon)
        return self

    def build(self):
        return self.character

    # Нужен reset
