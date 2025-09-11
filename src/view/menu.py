from common import WELCOME_TEXT, USER_LOGIN_FORM, MENU
from .view_helper.ViewManager import ViewManager


class MainMenuView:
    def __init__(self):
        pass

    def display_welcome(self):
        print(ViewManager.align_massive_center(WELCOME_TEXT))

    def display_login_form(self):
        print(ViewManager.align_massive_center(USER_LOGIN_FORM))

    def main_menu(self):
        menu = ViewManager.style_text(MENU).yellow
        print(ViewManager.align_massive_center(menu))
        
