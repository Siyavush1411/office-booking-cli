import sqlite3
from zlib import DEF_BUF_SIZE
from models import Booking
from database import BaseRepository


class BookingRepository(BaseRepository):
    def __init__(self):
        self.conn = sqlite3.connect("booking.db")
        self.c = self.conn.cursor()

    def add(self, booking: Booking):
        self.c.execute(
            "insert into booking (user_id, room_id, start_time, end_time) VALUES (?, ?, ?, ?)",
            (booking.username, booking.room_id, booking.start_date, booking.end_date, booking.email, booking.phone)
        )
        self.conn.commit()
    
    def get(self, booking_id):
        self.c.execute("select * from booking where id = ?", (booking_id,))
        row = self.c.fetchone()
        if row:
            return Booking(
                id=booking_id,
                room_id=row[1],
                username=row[2],
                email=row[3],
                phone=row[4],
                start_date=row[5],
                end_date=row[6]
            )
        return None

    def get_all(self):
        self.c.execute("select * from booking")
        rows = self.c.fetchall()
        bookings = []
        for row in rows:
            bookings.append(Booking(
                id=row[0],
                room_id=row[1],
                username=row[2],
                email=row[3],
                phone=row[4],
                start_date=row[5],
                end_date=row[6]
            ))
        return bookings or None

    def update(self, booking: Booking):
        self.c.execute(
            "update booking set room_id = ?, username = ?, email = ?, phone = ?, start_date = ?, end_date = ? where id = ?",
            (booking.room_id, booking.username, booking.email, booking.phone, booking.start_date, booking.end_date, booking.id)
        )
        self.conn.commit()

    def delete(self, booking_id):
        self.c.execute("delete from booking where id = ?", (booking_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()