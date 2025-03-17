from .builder import CharacterBuilder
from items.weapon import WeaponLoader
from config import settings
from enums import WeaponType, Race, CharacterClass


class CharacterDirector:
    def __init__(self, name: str):
        self.name = name
        self.builder = CharacterBuilder()
        self._init_default_weapons()

    def _init_default_weapons(self):
        weapon_for_start = WeaponLoader.load_from_config(f"{settings.SOURCE_LOAD_PATH}items_for_start.json")

        self.weapons = {
            WeaponType.SWORD: next((weapon for weapon in weapon_for_start if weapon.weapon_type == WeaponType.SWORD), None),
            WeaponType.STAFF: next((weapon for weapon in weapon_for_start if weapon.weapon_type == WeaponType.STAFF), None),
            WeaponType.BOW: next((weapon for weapon in weapon_for_start if weapon.weapon_type == WeaponType.BOW), None),
        }

    def create_human_warrior(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.HUMAN)
                .set_class(CharacterClass.WARRIOR)
                .add_weapon(self.weapons[WeaponType.SWORD])
                .build())

    def create_human_mage(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.HUMAN)
                .set_class(CharacterClass.MAGE)
                .add_weapon(self.weapons[WeaponType.STAFF])
                .build())

    def create_human_archer(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.HUMAN)
                .set_class(CharacterClass.ARCHER)
                .add_weapon(self.weapons[WeaponType.BOW])
                .build())

    def create_elf_warrior(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.ELF)
                .set_class(CharacterClass.WARRIOR)
                .add_weapon(self.weapons[WeaponType.SWORD])
                .build())

    def create_elf_mage(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.ELF)
                .set_class(CharacterClass.MAGE)
                .add_weapon(self.weapons[WeaponType.STAFF])
                .build())

    def create_elf_archer(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.ELF)
                .set_class(CharacterClass.ARCHER)
                .add_weapon(self.weapons[WeaponType.BOW])
                .build())

    def create_dwarf_warrior(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.DWARF)
                .set_class(CharacterClass.WARRIOR)
                .add_weapon(self.weapons[WeaponType.SWORD])
                .build())

    def create_dwarf_mage(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.DWARF)
                .set_class(CharacterClass.MAGE)
                .add_weapon(self.weapons[WeaponType.STAFF])
                .build())

    def create_dwarf_archer(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.DWARF)
                .set_class(CharacterClass.ARCHER)
                .add_weapon(self.weapons[WeaponType.BOW])
                .build())

    def create_orc_warrior(self):
        return (self.builder
                .set_name(self.name)
                .set_race(Race.ELF)
                .set_class(CharacterClass.WARRIOR)
                .add_weapon(self.weapons[WeaponType.SWORD])
                .build())

