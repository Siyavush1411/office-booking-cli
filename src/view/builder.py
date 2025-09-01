from .menu import MainMenuView


class ViewBuilder:
    def __init__(self):
        self.main_menu = MainMenuView()

    def start_menu(self):
        self.main_menu.display_welcome()
        self.main_menu.display_login_form()
