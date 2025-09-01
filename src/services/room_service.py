from models import Room
from common.table_constants import TABLE_ROOM_HEADER, TABLE_ROOM_BOTTOM, TABLE_ROOM_SEPPARATOR


class RoomService:
    def get_all_rooms(self) -> list:
        return Room.get_all()


class RoomDisplayService:
    def __init__(self):
        self.room_service = RoomService()

    def display_all_rooms(self):
        rooms = self.room_service.get_all_rooms()

        print(TABLE_ROOM_HEADER)
        for i, room in enumerate(rooms, start=0):
            status = "занята" if room.is_busy else "свободна"
            print(f"┃ {room.name:<29} ┃ {status:<24} ┃")
            if i != len(rooms) - 1:
                print(TABLE_ROOM_SEPPARATOR)
        print(TABLE_ROOM_BOTTOM)
