from common import WELCOME_TEXT, USER_LOGIN_FORM, CHOICE_ROOM
from view_helper import ViewManager


class MainMenuView:
    def __init__(self):
        pass

    def display_welcome(self):
        print(ViewManager.align_massive_center(WELCOME_TEXT))

    def display_login_form(self):
        print(ViewManager.align_massive_center(USER_LOGIN_FORM))


class RoomChoiceView:
    def __init__(self):
        pass

    def display_room_choice(self):
        print(ViewManager.align_massive_center(CHOICE_ROOM))

    def display_all_rooms(self):
        if not rooms:
            print("Нет доступных комнат.")
            return
        print("Доступные комнаты:")
        for room in rooms:
            print(f"- {room.name} (название)")