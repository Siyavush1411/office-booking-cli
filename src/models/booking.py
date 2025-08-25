from dataclasses import dataclass


@dataclass
class Booking:
    room_id: int
    username: str
    email: str
    phone: str
    start_date: str
    end_date: str
