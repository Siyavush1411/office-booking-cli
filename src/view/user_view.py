import os

from models import Room
from services.room_service import RoomDisplayService
from .menu import MainMenuView
from .utils.user_confirmations import UserConfirmations
from services.user_service import UserService
from models.user import User
from .utils.user_action_lazy_init import UserActionLazyInitialization




class ViewService:
    def __init__(self):
        self.main_menu = MainMenuView()

    def display_welcome(self):
        self.main_menu.display_welcome()

    def display_login_form(self):
        self.main_menu.display_login_form()

    def start(self):
        self.display_welcome()
        self.display_login_form()


class UserRegistrationView:
    def __init__(self):
        self.view_service = ViewService()
        self.user_confirmations = UserConfirmations()

    def register_user(self):
        username = input("Введите имя пользователя: ")
        password = self.user_confirmations._confirm_password()
        email = self.user_confirmations._confirm_email()
        phone = self.user_confirmations._confirm_phone()
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            username=username,
            password=password
        ).add()
        print(f"Регистрация пользователя {username} завершена.")
        return True


class UserLoginView:
    def __init__(self):
        self.view_service = ViewService()
        self.user_service = UserService()

    def login_user(self):
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        user = self.user_service.get_user_by_username(username)
        if not user or user.password != password:
            print("Неверное имя пользователя или пароль. Попробуйте еще раз.")
            return self.login_user()
        print(f"Пользователь {username} вошел в систему.")


class UserActionView(UserActionLazyInitialization):
    def display_user_dashboard(self):
        self.view_service.start()
        user_input = input("Нажмите 1 для регистрации или 2 для входа: ")
        is_success = self._user_auth_choice(user_input)
        if is_success:
            result = self._user_room_choice()
            selected_room = Room.get("id", result)
            selected_room.update(selected_room.id, is_busy=True),

    def _user_auth_choice(self, user_input: str):
        if user_input == "1":
            self.user_registration.register_user()
        elif user_input == "2":
            self.user_login.login_user()
        else:
            user_input = input("Неверный ввод. Пожалуйста, нажмите 1 для регистрации или 2 для входа: ")
            os.system('cls' if os.name == 'nt' else 'clear')
            self._user_auth_choice(user_input)
        return True

    def _user_room_choice(self):
        self.room_display.display_all_rooms()
        user_input = input("Выберите номер комнаты: ")
        rooms = Room.get_all()
        try:
            choice = int(user_input)
        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Введите число.")
            return None
        if 1 <= choice <= len(rooms):
            if rooms[choice - 1].is_busy:
                os.system('cls' if os.name == 'nt' else 'clear')
                return self._user_room_choice()
                print("Комната занята. Пожалуйста, выберите другую комнату.")
            return choice
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Неверный ввод. Пожалуйста, выберите номер комнаты из списка.")
            return None
