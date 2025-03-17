from abc import ABC, abstractmethod
from character.create_character.director import CharacterDirector
import random


class GameState(ABC):
    @abstractmethod
    def handle(self, controller):
        pass


class MainMenuState(GameState):
    def handle(self, controller):
        print(f"Добро пожаловать, {controller.user if controller.user else 'Игрок'}!")
        print("1) Авторизоваться\n2) Выйти")
        choice = input("> ")

        actions = {
            "1": lambda: controller.change_state(AuthState()),
            "2": controller.exit
        }

        action = actions.get(choice, lambda: print("Действие не распознано"))
        action()


class AuthState(GameState):
    def handle(self, controller):
        print(f"Авторизовация!")
        login = input("Введите логин:")
        password = input("Введите пароль:")
        controller.change_state(CreateCharacter())


class CreateCharacter(GameState):
    def handle(self, controller):
        print("На вашем аккаунте нет персонажей, создайте его!")
        name = input("Введите ник: ")
        director = CharacterDirector(name=name)

        print("1) Раса Человек, Класс Маг")
        print("2) Раса Человек, Класс Воин")
        print("3) Раса Человек, Класс Лучник")
        print("4) Раса Эльф, Класс Маг")
        print("5) Раса Эльф, Класс Воин")
        print("6) Раса Эльф, Класс Лучник")

        choice = input("Сделайте свой выбор [1,2,3,4,5,6]: ")

        actions = {
            "1": director.create_human_mage(),
            "2": director.create_human_warrior(),
            "3": director.create_human_archer(),
            "4": director.create_elf_mage(),
            "5": director.create_elf_warrior(),
            "6": director.create_elf_archer(),
        }

        char = actions.get(choice)
        controller.char = char
        if char:
            print(f"\nДобро пожаловать в игру == {controller.char.name}  == \n")
            controller.change_state(GameplayState())
        else:
            print("Выбор не распознан, попробуйте снова.")
            self.handle(controller)


class GameplayState(GameState):
    def handle(self, controller):
        print("\n🏰 Ты находишься в городе. Что хочешь сделать?")
        print("1) Исследовать окрестности")
        print("2) Поговорить с Телепортером")
        print("3) Осмотреть себя")
        print("4) Выйти из игры")

        choice = input("Выбери действие [1,2,3]: ")

        actions = {
            "1": lambda: print("🌿 Ты осматриваешься вокруг... и видешь одни перспективы для твоего развития"),
            "2": lambda: controller.change_state(TeleporterState()),  # Переход к Телепортеру
            "3": controller.char.show_status(),  # Переход к Телепортеру
            "4": controller.exit
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))

        if choice == "1" or "3":
            print("\nСпрашиваю еще раз")
            self.handle(controller)
        else:
            action()


class TeleporterState(GameState):
    def handle(self, controller):
        print("\n✨ Добро пожаловать, путешественник! Я Телепортер. ✨")
        print("Я могу отправить тебя в одну из четырех тренировочных зон:")
        print("1) Лес Древних – место, полное тайн и магии.")
        print("2) Грозовой Каньон – испытание для самых выносливых.")
        print("3) Огненные Пещеры – опасное место, полное лавы и монстров.")
        print("4) Ледяные Пустоши – суровый край вечного холода.")
        print("5) Вернуться в город.")

        choice = input("Куда хочешь отправиться? [1,2,3,4,5]: ")

        actions = {
            "1": lambda: self.teleport(controller, "Лес Древних", choice),
            "2": lambda: self.teleport(controller, "Грозовой Каньон", choice),
            "3": lambda: self.teleport(controller, "Огненные Пещеры", choice),
            "4": lambda: self.teleport(controller, "Ледяные Пустоши", choice),
            "5": lambda: controller.change_state(GameplayState())  # Возвращение в игру
        }

        action = actions.get(choice)
        if action:
            action()
        else:
            print("❌ Ошибка: Такой зоны нет! Попробуй снова.")
            self.handle(controller)

    def teleport(self, controller, location, choice):
        print(f"🌟 Телепортирую в {location}... Добро пожаловать! 🌟")
        actions = {
            "1": lambda: controller.change_state(AncientForestState()),
            "2": lambda: controller.change_state(ThunderCanyonState()),
            "3": lambda: controller.change_state(FireCavesState()),
            "4": lambda: controller.change_state(IceWastesState()),
            "5": lambda: controller.change_state(GameplayState())
        }

        actions.get(choice)()


class BattleState(GameState):
    def __init__(self, monster_name, monster_hp):
        self.monster_name = monster_name
        self.monster_hp = monster_hp

    def handle(self, controller):
        print(f"\n⚔️ Ты вступаешь в бой с {self.monster_name}! ⚔️")
        print(f"У {self.monster_name} {self.monster_hp} HP!")

        while self.monster_hp > 0:
            print("\n1) Атаковать 🗡️")
            print("2) Бежать 🏃‍♂️")

            choice = input("Выбери действие [1,2]: ")

            if choice == "1":
                damage = int(controller.char.attack_damage)
                self.monster_hp -= damage
                print(f"Твое здоровье {controller.char.current_hp}")
                print(f"💥 Ты нанес {damage} урона! У {self.monster_name} осталось {max(self.monster_hp, 0)} HP!")
                mob_damage = random.randint(1, 500)
                controller.char.take_damage(mob_damage)

                print(f"\n💥 {self.monster_name} нанес тебе {mob_damage}")
                if not controller.char.current_hp:
                    print(f"Ты погиб, твое HP ==  {controller.char.current_hp}")
                    print(f"Возвращаю в город")
                    controller.change_state(GameplayState())
                if self.monster_hp <= 0:
                    print(f"🎉 Ты победил {self.monster_name}! 🏆")
                    controller.change_state(GameplayState())
                    return
            elif choice == "2":
                print("😨 Ты сбежал с поля боя и вернулся в город.")
                controller.change_state(GameplayState())
                return
            else:
                print("❌ Ошибка: Действие не распознано!")


class AncientForestState(GameState):
    def handle(self, controller):
        print("\n🌲 Ты попал в Лес Древних – место магии и тайн.")
        print("1) Исследовать лес")
        print("2) Сразиться с Древним Духом 👻")
        print("3) Вернуться в город")

        choice = input("Выбери действие [1,2,3]: ")

        actions = {
            "1": self.explore_forest,
            "2": lambda: controller.change_state(BattleState("Древний Дух", 30)),
            "3": lambda: controller.change_state(GameplayState())
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))
        action()

    def explore_forest(self, controller):
        events = [
            "🌿 Ты нашел древний амулет, он испускает слабый свет!",
            "🦉 Ты услышал шепот деревьев, но не разобрал слов...",
            "🐺 Из кустов выбежал волк! К счастью, он тебя не заметил.",
            "🔮 Ты обнаружил алтарь магии, твои силы немного восстановились!"
        ]
        print(random.choice(events))


class ThunderCanyonState(GameState):
    def handle(self, controller):
        print("\n⛈ Ты оказался в Грозовом Каньоне – испытание для выносливых.")
        print("1) Осмотреться")
        print("2) Сразиться с Громовым Великаном ⚡")
        print("3) Вернуться в город")

        choice = input("Выбери действие [1,2,3]: ")

        actions = {
            "1": self.explore_canyon,
            "2": lambda: controller.change_state(BattleState("Громовой Великан", 40)),
            "3": lambda: controller.change_state(GameplayState())
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))
        action()

    def explore_canyon(self, controller):
        events = [
            "⚡ Молния ударила в камень рядом с тобой – будь осторожен!",
            "🏺 Ты нашел древний сосуд с неизвестной жидкостью.",
            "🌀 Ветер усиливается, тебя начинает сносить с тропы!",
            "💎 Под камнем ты обнаружил маленький драгоценный камень."
        ]
        print(random.choice(events))


class FireCavesState(GameState):
    def handle(self, controller):
        print("\n🔥 Ты попал в Огненные Пещеры – здесь жарко и опасно!")
        print("1) Войти глубже в пещеры")
        print("2) Сразиться с Огненным Демоном 🔥")
        print("3) Вернуться в город")

        choice = input("Выбери действие [1,2,3]: ")

        actions = {
            "1": self.explore_cave,
            "2": lambda: controller.change_state(BattleState("Огненный Демон", 50)),
            "3": lambda: controller.change_state(GameplayState())
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))
        action()

    def explore_cave(self, controller):
        events = [
            "🔥 Ты нашел старый меч, опаленный пламенем.",
            "💀 В пещере лежат кости, чей-то последний поход...",
            "💎 Ты обнаружил рубин, мерцающий в темноте!",
            "🌋 Земля дрожит – кажется, скоро начнется извержение!"
        ]
        print(random.choice(events))


class IceWastesState(GameState):
    def handle(self, controller):
        print("\n❄️ Ты оказался в Ледяных Пустошах – суровом краю вечного холода.")
        print("1) Разведать местность")
        print("2) Сразиться с Ледяным Големом ❄️")
        print("3) Вернуться в город")

        choice = input("Выбери действие [1,2,3]: ")

        actions = {
            "1": self.explore_ice_wastes,
            "2": lambda: controller.change_state(BattleState("Ледяной Голем", 35)),
            "3": lambda: controller.change_state(GameplayState())
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))
        action()

    def explore_ice_wastes(self, controller):
        events = [
            "🧊 Лед треснул под твоими ногами, но ты успел увернуться!",
            "🥶 Вдалеке ты заметил таинственный силуэт, но он исчез...",
            "🦴 Ты нашел останки древнего существа.",
            "🌟 Среди снегов ты обнаружил сверкающий ледяной кристалл."
        ]
        print(random.choice(events))
