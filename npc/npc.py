from random import choice, randint
from functools import wraps


def check_hp(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.hp < 0:
            self.hp = 0
        return func(self, *args, **kwargs)

    return wrapper


def attack_phrase_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        phrases = [
            "Ты не устоишь перед моей мощью!",
            "Готовься к поражению!",
            "Тебе не победить меня!",
            "Сейчас будет больно!",
            "Я не позволю тебе победить!"
        ]
        print(f"🛡️ {self.name} говорит: {choice(phrases)}")
        return func(self, *args, **kwargs)
    return wrapper


class NPC:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.base_damage = 35

    def get_chance_crit_damage(self):
        return randint(5, self.base_damage)

    @attack_phrase_decorator
    def give_damage(self):
        return self.base_damage + self.get_chance_crit_damage()

    def take_damage(self, amount: int) -> None:
        self.hp = self.base_damage = self.base_damage - amount

    def get_hp(self) -> int:
        return self.hp

    def get_name(self) -> str:
        return self.name

    @check_hp
    def __str__(self):
        return f"{self.name} (❤️ {self.hp})"
