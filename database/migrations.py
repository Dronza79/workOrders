from peewee import SqliteDatabase

from .models import Worker, Task, Period, Vacancy, Status, Order, FUNC_VARIABLES, STATUS_VARIABLES
from .settings import path, get_database

models = (
    Vacancy,
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
            Vacancy.insert_many([[func] for func in FUNC_VARIABLES.values()], fields=['post']).execute()
        if not list(Status.select()):
            Status.insert_many([[value] for value in STATUS_VARIABLES.values()], ['state']).execute()


def reconnect_database():
    for model in models:
        model._meta.database.close()
        model._meta.database = get_database()
        model._meta.database.connect()
