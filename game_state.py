from abc import ABC, abstractmethod
from character.create_character.director import CharacterDirector
import random
from npc.npc import NPC
from items.item import add_money_to_inventory


class GameState(ABC):
    @abstractmethod
    def handle(self, controller):
        pass


class MainMenuState(GameState):
    def handle(self, controller):
        print(f"Добро пожаловать, {controller.user if controller.user else 'Игрок'}!")
        print("1) Авторизоваться\n2) Выйти")
        choice = input("> ")
        # Input/Output должен быть дополнительным уровнем абстракции. Может быть стоило сделать Bridge хоть самый упрощенный

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

        choice = input("Выбери действие [1,2,3,4]: ")

        actions = {
            "1": print("🌿 Ты осматриваешься вокруг... и видешь одни перспективы для твоего развития"),
            "2": lambda: controller.change_state(TeleporterState()),
            "3": print(controller.char.show_status()),
            "4": lambda: controller.exit
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))

        if choice == "1" or choice == "3":
            controller.change_state(GameplayState())
        else:
            action()


class TeleporterState(GameState):
    def handle(self, controller):
        print("\n✨ Добро пожаловать, путешественник! Я Телепортер. ✨")
        print("Я могу отправить тебя в одну из тренировочных зон:")

        locations = controller.location

        for num, location_info in locations.items():
            name = location_info['name']
            desc = location_info['description']
            difficulty = location_info['difficulty']
            print(f"\n{num}) {name} – {desc} (Сложность: {difficulty})")

        print("\n5) Вернуться в город.")

        choice = input("Куда хочешь отправиться? [1,2,3,4,5]: ")

        if choice in locations:
            location_info = locations[choice]
            name = location_info['name']
            description = location_info['description']
            difficulty = location_info['difficulty']

            npc_info = location_info['npc']
            npc = NPC(npc_info['name'], npc_info['hp'])

            events = location_info.get('events', [])

            self.teleport(controller, name, description, difficulty, npc, events)
        elif choice == "5":
            controller.change_state(GameplayState())
        else:
            print("❌ Ошибка: Такой зоны нет! Попробуй снова.")
            self.handle(controller)

    def teleport(self, controller, location, description, difficulty, npc, events):
        print(f"🌟 Телепортирую в {location}... Добро пожаловать! 🌟")
        controller.change_state(ExplorationState(location, npc, description, difficulty, events))


class BattleState(GameState):
    def __init__(self, monster_name, monster_hp):
        self.npc = NPC(monster_name, monster_hp)

    def handle(self, controller):
        print(f"\n⚔️ Ты вступаешь в бой с {self.npc.name}! ⚔️")
        print(f"У {self.npc.name} {self.npc.hp} HP!")

        while self.npc.hp > 0:
            print("\n1) Атаковать 🗡️")
            print("2) Бежать 🏃‍♂️")

            choice = input("Выбери действие [1,2]: ")

            if choice == "1":
                damage = int(controller.char.attack_damage)
                self.npc.hp -= damage
                print(f"Твое здоровье {controller.char.current_hp} HP")
                print(f"\n🔥  Ты нанес {damage} урона! У {self.npc.name} осталось {self.npc.hp} HP!")
                mob_damage = self.npc.give_damage()
                controller.char.take_damage(mob_damage)

                print(f"\n💥 {self.npc.name} нанес тебе {mob_damage}")
                if not controller.char.current_hp:
                    print(f"Ты погиб, твое HP ==  {controller.char.current_hp}")
                    print(f"Возвращаю в город 🏙️")
                    controller.change_state(GameplayState())
                if self.npc.hp <= 0:
                    print(f"🎉 Ты победил {self.npc.name}! 🏆")
                    # Победа над монстром - получаем случайную награду
                    self.reward_player(controller)
                    controller.change_state(GameplayState())
                    return
            elif choice == "2":
                print("😨 Ты сбежал с поля боя и вернулся в город.")
                controller.change_state(GameplayState())
                return
            else:
                print("❌ Ошибка: Действие не распознано!")

    def reward_player(self, controller):
        money_reward = random.randint(500, 1500)
        exp_reward = random.randint(20, 100)
        controller.char.gain_exp(exp_reward)
        add_money_to_inventory(controller, money_reward)

        print(f"🎉 Ты получил {money_reward} 💰 монет и {exp_reward} ✨ опыта!")


class ExplorationState(GameState):
    def __init__(self, location_name, npc, description, difficulty, events):
        self.location_name = location_name
        self.npc = npc
        self.description = description
        self.difficulty = difficulty
        self.events = events

    def handle(self, controller):
        print(f"\n🌍 {self.location_name} – исследуй и сражайся!")
        print(f"Описание: {self.description}")
        print(f"Сложность: {self.difficulty}")

        print("\n1) Осмотреться")
        print(f"2) Сразиться с {self.npc.name}")
        print("3) Вернуться в город")

        choice = input("Выбери действие [1,2,3]: ")

        actions = {
            "1": lambda: self.explore(controller),
            "2": lambda: controller.change_state(BattleState(self.npc.name, self.npc.hp)),
            "3": lambda: controller.change_state(GameplayState())
        }

        action = actions.get(choice, lambda: print("❌ Ошибка: Действие не распознано!"))
        action()

    def explore(self, controller):
        print(f"\n{random.choice(self.events)}")
        controller.change_state(ExplorationState(self.location_name,
                                                 self.npc,
                                                 self.description,
                                                 self.difficulty,
                                                 self.events
                                                 )
                                )
