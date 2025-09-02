from services.room_service import RoomDisplayService
from ..user_view import UserRegistrationView, UserLoginView, ViewService


class UserActionLazyInitialization:
    def __init__(self):
        self._view_service = None
        self._user_registration = None
        self._user_login = None
        self._room_display = None

    @property
    def view_service(self):
        if self._view_service is None:
            self._view_service = ViewService()
        return self._view_service

    @property
    def user_registration(self):
        if self._user_registration is None:
            self._user_registration = UserRegistrationView()
        return self._user_registration

    @property
    def user_login(self):
        if self._user_login is None:
            self._user_login = UserLoginView()
        return self._user_login

    @property
    def room_display(self):
        if self._room_display is None:
            self._room_display = RoomDisplayService()
        return self._room_display
