import models
from models import Room
from .migrations import Migration


def init_db():
    classes = [getattr(models, name) for name in models.__all__]
    Migration(cls=classes).migrate()
    if Room.get('id', 5) is None:
        for i in range(4):
            Room(
                name=f"Комната {i + 1}"
            )
