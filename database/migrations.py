from .models import (
    Worker, Task, Period, Vacancy, Status, Order, TypeTask,
    FUNC_VARIABLES, STATUS_VARIABLES, TYPE_VARIABLES, ProgramSetting
)
from .settings import get_database

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


def reconnect_database():
    for model in models:
        model._meta.database.close()
        model._meta.database = get_database()
        model._meta.database.connect()


def migrations_v1_1_0():
    try:
        from peewee import CharField
        from playhouse.migrate import SqliteMigrator, migrate

        db = get_database()
        db.create_tables([ProgramSetting])
        if not ProgramSetting.select().count():
            print('Создаю запись настроек')
            ProgramSetting.create(
                major=1,
                minor=1,
                patch=0,
                org='ООО ЭНЕРГОЭРА',
                div='Участок электромонтажа',
                resp_post='',
                resp_name='',
                head_post='',
                head_name='',
            )
        if 'ordinal' not in [col.name for col in db.get_columns('worker')]:
            migrator = SqliteMigrator(db)
            new_col = CharField(null=True)
            with db.atomic():
                migrate(migrator.add_column('worker', 'ordinal', new_col))
    except Exception as ex:
        print(f'{ex=}')
