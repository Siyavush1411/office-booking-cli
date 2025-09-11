from models import Room
from common.table_constants import TABLE_ROOM_HEADER, TABLE_ROOM_BOTTOM, TABLE_ROOM_SEPPARATOR
from view.view_helper.ViewManager import ViewManager


class RoomService:
    def get_all_rooms(self) -> list:
        return Room.get_all()


class RoomDisplayService:
    def __init__(self):
        self.room_service = RoomService()
        self.view_manager = ViewManager()

    def display_all_rooms(self):
        rooms = self.room_service.get_all_rooms()
        is_busy: str = self.view_manager.style_text("свободна").green
        is_free: str = self.view_manager.style_text("занята").red
        print(TABLE_ROOM_HEADER)
        for i, room in enumerate(rooms, start=0):
            status = is_free if room.is_busy else is_busy
            print(f"┃ {room.name:<29} ┃ {self.view_manager.pad_ansi(status, 24)} ┃")
            if i != len(rooms) - 1:
                print(TABLE_ROOM_SEPPARATOR)
        print(TABLE_ROOM_BOTTOM)
