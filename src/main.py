import atexit

from database import init_db
from view.user_view import UserActionView
from services.room_checker import start_background_checker, stop_background_checker

from models import Booking, Room


def main():
    init_db()
    rooms = Room.get_all()
    if not rooms or len(rooms) < 5:
        for i in range(5):
            Room(
                name=f"Комната {i + 1}"
            ).add()

    start_background_checker()
    
    atexit.register(stop_background_checker)

    user_action_view = UserActionView()
    user_action_view.display_user_dashboard()


if __name__ == "__main__":
    main()