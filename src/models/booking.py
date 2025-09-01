from dataclasses import dataclass, field
from database.base_model import BaseModel


@dataclass
class Booking(BaseModel):
    id: int | None = field(default=0, init=False)
    room_id: int
    user_id: int
    email: str
    phone: str
    start_date: str
    end_date: str

    foreign_keys = {"room_id": ("room", "id"), "user_id": ("user", "id")}
