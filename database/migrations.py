import importlib

from .models import *
from .config import get_database

models = (
    Vacancy,
    TypeTask,
    Worker,
    Status,
    Order,
    Task,
    Period,
    ProgramSetting
)


def apply_migrations():
    db = get_database()
    db.create_tables(models)
    with db.atomic():
        if not list(Vacancy.select()):
            Vacancy.insert_many(FUNC_VARIABLES).execute()
        if not list(Status.select()):
            Status.insert_many(STATUS_VARIABLES).execute()
        if not list(TypeTask.select()):
            TypeTask.insert_many(TYPE_VARIABLES).execute()
    db.close()


def change_database():
    for model in importlib.import_module('database.models').models:
        model._meta.database = get_database()


def migrations_v1_1_0():

    db = get_database()
    try:
        from peewee import CharField
        from playhouse.migrate import SqliteMigrator, migrate

        if 'ordinal' not in [col.name for col in db.get_columns('worker')]:
            migrator = SqliteMigrator(db)
            new_col = CharField(null=True)
            with db.atomic():
                migrate(migrator.add_column('worker', 'ordinal', new_col))
    except Exception as ex:
        print(f'{ex=}')


def migrations_v2_0_0():
    db = get_database()
    try:
        from peewee import CharField
        from playhouse.migrate import SqliteMigrator, migrate

        if 'm_theme' not in [col.name for col in db.get_columns('programsetting')]:
            migrator = SqliteMigrator(db)
            new_col = CharField(null=True)
            with db.atomic():
                migrate(migrator.add_column('programsetting', 'm_theme', new_col))
    except Exception as ex:
        print(f'{ex=}')


