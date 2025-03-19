from abc import ABC, abstractmethod
from enums import TypeReward


class RewardHandler(ABC):
    @abstractmethod
    def handle_reward(self, reward_type, amount):
        pass


class MoneyRewardHandler(RewardHandler):
    def handle_reward(self, reward_type, amount):
        if reward_type == TypeReward.MONEY:
            print(f"Вы получили {amount} монет!")
        else:
            self.next_handler.handle_reward(reward_type, amount)

    def set_next(self, handler):
        self.next_handler = handler


class ExperienceRewardHandler(RewardHandler):
    def handle_reward(self, reward_type, amount):
        if reward_type == TypeReward.EXP:
            print(f"Вы получили {amount} опыта!")
        else:
            self.next_handler.handle_reward(reward_type, amount)

    def set_next(self, handler):
        self.next_handler = handler
