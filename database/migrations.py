from peewee import SqliteDatabase

from .models import Worker, Task, Period, Vacancy, Status, Order
from .utils import path, get_database

models = (
    Vacancy,
    Worker,
    Status,
    Order,
    Task,
    Period,
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
