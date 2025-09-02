from database import init_db
from view.user_view import UserActionView


def main():
    init_db()

    user_action_view = UserActionView()

    user_action_view.display_user_dashboard()


if __name__ == "__main__":
    main()
