from peewee import SqliteDatabase

from .models import (
    Worker, Task, Period, Vacancy, Status, Order, TypeTask,
    FUNC_VARIABLES, STATUS_VARIABLES, TYPE_VARIABLES
)
from .settings import path, get_database

models = (
    Vacancy,
    TypeTask,
    Worker,
    Status,
    Order,
    Task,
    Period,
)


def apply_migrations():
    db = SqliteDatabase(path.get_path, pragmas={'foreign_keys': 1})
    db.create_tables(models)
    with get_database().atomic():
        if not list(Vacancy.select()):
            Vacancy.insert_many(FUNC_VARIABLES).execute()
        if not list(Status.select()):
            Status.insert_many(STATUS_VARIABLES).execute()
        if not list(TypeTask.select()):
            TypeTask.insert_many(TYPE_VARIABLES).execute()


def reconnect_database():
    for model in models:
        model._meta.database.close()
        model._meta.database = get_database()
        model._meta.database.connect()
