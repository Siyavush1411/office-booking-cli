from dataclasses import dataclass, field
from database.base_model import BaseModel


@dataclass
class User(BaseModel):
    id: int | None = field(default=0, init=False)
    email: str
    phone: str
    username: str
    password: str
