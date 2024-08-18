from peewee import SqliteDatabase

from .models import Person, WorkTask, WorkLapse, FuncPosition, Turn, Status, ProductionOrder
from .utils import path, get_database

models = (
    FuncPosition,
    Person,
    Status,
    ProductionOrder,
    WorkTask,
    WorkLapse,
    # Turn
)


def apply_migrations():
    db = SqliteDatabase(path.get_path, pragmas={'foreign_keys': 1})
    db.create_tables(models)


def reconnect_database():
    for model in models:
        model._meta.database.close()
        model._meta.database = get_database()
        model._meta.database.connect()
