import os
from datetime import datetime, timedelta

from models import Room, User, Booking
from .menu import MainMenuView
from .utils.user_confirmations import UserConfirmations
from .utils.user_action_lazy_init import UserActionLazyInitialization
from services.user_service import UserService
from services import add_to_notification
from common import save_current_user_to_session, get_current_user_from_session


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
        User(
            email=email,
            phone=phone,
            username=username,
            password=password,
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
        save_current_user_to_session(user_id=user.id)


class UserActionView(UserActionLazyInitialization):
    def display_user_dashboard(self):
        self.view_service.start()
        user_input = input("Нажмите 1 для регистрации или 2 для входа: ")
        is_success = self._user_auth_choice(user_input)
        if is_success:
            result = self._user_room_choice()
            selected_room = Room.get("id", result)
            self.booking_room(room_id=selected_room.id)
            selected_room.update(selected_room.id, is_busy=True)
            print("Комната успешно забронирована! Мы пришлем уведомление при освобождении комнаты.")

    def booking_room(self, room_id: int):
        user_id = get_current_user_from_session()
        start_time = datetime.now()
        hours = self._set_hours()
        minutes = self._set_minutes(room_id=room_id)
        end_time = start_time + timedelta(hours=hours, minutes=minutes)
        Booking(
            room_id=room_id,
            user_id=user_id,
            start_time=start_time.strftime("%Y-%m-%d %H:%M"),
            end_time=end_time.strftime("%Y-%m-%d %H:%M"),
        ).add()

    def _set_hours(self):
        hours = int(input("На сколько часов: ") or 0)
        if hours > 24:
            os.system("cls" if os.name == "nt" else "clear")
            print("Нельзя занимать комнату больше 24 часов. Попробуйте еще раз.")
            return self._set_hours()
        return hours

    def _set_minutes(self, room_id: int):
        minutes = int(input("На сколько минут. нажмите -1 чтобы вернутся в вводу часов: ") or 0)
        if minutes == -1:
            return self.booking_room(room_id=room_id)
        if minutes > 60:
            os.system("cls" if os.name == "nt" else "clear")
            print("В этой вселенной час не растянется больше чем на 60 минут. Попробуйте в другой вселенной.")
            return self._set_minutes()
        return minutes

    def _user_auth_choice(self, user_input: str):
        if user_input == "1":
            self.user_registration.register_user()
        elif user_input == "2":
            self.user_login.login_user()
        else:
            user_input = input(
                "Неверный ввод. Пожалуйста, нажмите 1 для регистрации или 2 для входа: "
            )
            os.system("cls" if os.name == "nt" else "clear")
            self._user_auth_choice(user_input)
        return True

    def _user_room_choice(self):
        self.room_display.display_all_rooms()
        user_input = input("Выберите номер комнаты: ")
        rooms = Room.get_all()
        try:
            choice = int(user_input)
        except ValueError:
            os.system("cls" if os.name == "nt" else "clear")
            print("Введите число.")
            return None
        if 1 <= choice <= len(rooms):
            if rooms[choice - 1].is_busy:
                os.system("cls" if os.name == "nt" else "clear")
                self._notification_choice(room_id=rooms[choice - 1].id)
                return self._user_room_choice()
            return choice
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("Неверный ввод. Пожалуйста, выберите номер комнаты из списка.")
            return None

    def _notification_choice(self, room_id: int): 
        user_id = get_current_user_from_session()
        print(
            "Комната занята. Уведомить вас при освобождении комнаты?\n 1 - да\t 2 - нет"
        )
        user_input = input("Введите число:")
        if user_input == "1":
            add_to_notification(user_id, room_id)
        elif user_input == "2":
            pass
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("Неверный ввод. Пожалуйста, введите 1 или 2.")
            self._notification_choice()

