from models import Room, Booking, User
from common.table_constants import (
    TABLE_ROOM_HEADER,
    TABLE_ROOM_BOTTOM,
    TABLE_ROOM_SEPPARATOR,
)


class BookingService:
    def get_all_bookings(self) -> list:
        booking = Booking.get_all()
        return booking


class BookingDisplayService:
    def __init__(self):
        self.booking_service = BookingService()

    def display_all_bookings(self):
        bookings = self.booking_service.get_all_bookings()
        print(bookings)
        print('┏' + '━' * 80 + '┓')
        for i, booking in enumerate(bookings, start=0):
            user = User.get("id", booking.user_id)
            if user is None:
                user = "Пользователь удален"
            else:
                user = user.username
            room = Room.get("id", booking.room_id)
            status = "занята" if booking.is_actual else "свободна"
            print(f"┃ {room.name:<29} ┃ {user:<24} ┃ {status:<19} ┃")
            if i != len(bookings) - 1:
                print('┣' + '━' * 80 + '┫')
        print('┗' + '━' * 80 + '┛')
