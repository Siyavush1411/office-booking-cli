from dataclasses import dataclass, field
from database.base_model import BaseModel


@dataclass
class Room(BaseModel):
    id: int | None = field(default=0, init=False)
    name: str
    is_busy: bool = False