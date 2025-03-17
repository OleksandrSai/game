from prompt_toolkit.shortcuts import checkboxlist_dialog, input_dialog
import json
from config import settings
from enums import LoadSource
from .user_loader import ApiUserLoader, LocalUserLoader


class AuthState(GameState):
    def handle(self, context):
        choice = checkboxlist_dialog(
            title="Добро пожаловать!",
            text="Выберите действие:",
            values=[("login", "Войти"), ("register", "Регистрация")]
        ).run()

        if not choice:
            return

        if "login" in choice:
            self._login(context)
        elif "register" in choice:
            self._register(context)

    def _login(self, context):
        email = input_dialog(title="Вход", text="Email:").run()
        password = input_dialog(title="Вход", text="Пароль:", password=True).run()

        user = next((u for u in context.users if u["email"] == email and u["password"] == password), None)
        if user:
            context.current_user = user
            context.set_state(CharacterMgmtState())
            print("Успешный вход!")
        else:
            print("Ошибка аутентификации!")

    def _register(self, context):
        email = input_dialog(title="Регистрация", text="Email:").run()
        password = input_dialog(title="Регистрация", text="Пароль:", password=True).run()

        if any(u["email"] == email for u in context.users):
            print("Пользователь уже существует!")
            return

        new_user = {
            "email": email,
            "password": password,
            "characters": []
        }
        context.users.append(new_user)
        context.save_users()
        context.current_user = new_user
        context.set_state(CharacterMgmtState())
        print("Регистрация успешна!")