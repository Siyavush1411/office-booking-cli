from database import init_db
from services.room_service import RoomDisplayService
from models.room import Room


def main():
    init_db()
    RoomDisplayService().display_all_rooms()


if __name__ == "__main__":
    main()
