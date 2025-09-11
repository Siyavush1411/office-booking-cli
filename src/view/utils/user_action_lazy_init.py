from services.room_service import RoomDisplayService


class UserActionLazyInitialization:
    def __init__(self):
        self._view_service = None
        self._user_registration = None
        self._user_login = None
        self._room_display = None

    @property
    def view_service(self):
        if self._view_service is None:
            from view.user_view import ViewService
            self._view_service = ViewService()
        return self._view_service

    @property
    def user_registration(self):
        if self._user_registration is None:
            from view.user_view import UserRegistrationView
            self._user_registration = UserRegistrationView()
        return self._user_registration

    @property
    def user_login(self):
        if self._user_login is None:
            from view.user_view import UserLoginView
            self._user_login = UserLoginView()
        return self._user_login

    @property
    def room_display(self):
        if self._room_display is None:
            self._room_display = RoomDisplayService()
        return self._room_display
    
    @property
    def main_menu(self):
        if self._main_menu is None:
            from view.menu import MainMenuView
            self._main_menu = MainMenuView()
        return self._main_menu

