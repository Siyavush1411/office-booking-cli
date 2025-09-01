from common import WELCOME_TEXT, USER_LOGIN_FORM
from view_helper.TextLayout import TextMarkupBuilder
from view_helper import ViewManager


class MainMenuView:
    def __init__(self):
        pass

    def display_welcome(self):
        print(ViewManager.align_massive_center(WELCOME_TEXT))

    def display_login_form(self):
        print(ViewManager.align_massive_center(USER_LOGIN_FORM))