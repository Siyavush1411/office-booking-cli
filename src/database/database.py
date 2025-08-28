from .migrations import Migration
import models


def init_db():
    classes = [getattr(models, name) for name in models.__all__]
    Migration(cls=classes).migrate()
