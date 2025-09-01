from models import user
from .menu import RoomChoiceView
from .menu import MainMenuView
from .utils.user_confirmations import UserConfirmations
from service import UserService
from models.user import User


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


class UserActionView:
    def __init__(self):
        self.view_service = ViewService()
        self.user_registration = UserRegistrationView()
        self.user_login = UserLoginView()

    def display_user_dashboard(self):
        self.view_service.start()
        user_input = input("Нажмите 1 для регистрации или 2 для входа: ")
        is_success = self._user_auth_choice(user_input)
        if is_success:
            RoomChoiceView().display_room_choice()

    def _user_auth_choice(self, user_input: str):
        if user_input == "1":
            self.user_registration.register_user()
        elif user_input == "2":
            self.user_login.login_user()
        else:
            user_input = input("Неверный ввод. Пожалуйста, нажмите 1 для регистрации или 2 для входа: ")
            self._user_auth_choice(user_input)
        return True
