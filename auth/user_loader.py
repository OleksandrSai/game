import os
import json
from abc import ABC, abstractmethod
from config import settings


class UserLoader(ABC):
    @abstractmethod
    def load_users(self):
        raise NotImplementedError


class LocalUserLoader(UserLoader):
    def __init__(self, filename=settings.USERS_LOCAL_PATH):
        self.filename = filename

    def load_users(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            return json.load(f)


class ApiUserLoader(UserLoader):
    def load_users(self):
        print("Загрузка пользователей из API...")
        raise NotImplementedError
