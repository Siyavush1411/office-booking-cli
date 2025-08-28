import sqlite3


def init_db():
    conn = sqlite3.connect("booking.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()
