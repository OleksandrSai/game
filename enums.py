from enum import Enum, auto


class TypeReward(Enum):
    EXP = auto(),
    MONEY = auto()


class LoadSource(Enum):
    LOCAL = auto()
    API = auto()


class ItemType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    CONSUMABLE = auto()
    MONEY = auto()


class WeaponType(Enum):
    SWORD = auto()
    AXE = auto()
    BOW = auto()
    STAFF = auto()
    DAGGER = auto()


class DamageType(Enum):
    PHYSICAL = auto()
    MAGICAL = auto()
    PIERCING = auto()


class ArmorSlot(Enum):
    WEAPON = auto()
    HELMET = auto()
    CHEST = auto()
    GLOVES = auto()
    PANTS = auto()
    BOOTS = auto()


class CharacterClass(Enum):
    WARRIOR = auto()
    MAGE = auto()
    ARCHER = auto()


class Race(Enum):
    HUMAN = auto()
    ELF = auto()
    DWARF = auto()
