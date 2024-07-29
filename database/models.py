import datetime

from peewee import *

from .utils import get_database


class BaseModel(Model):
    create_at = DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания')
    update_at = DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения')

    class Meta:
        database = get_database()
        only_save_dirty = True

    def save(self, **kwargs):
        self.update_at = datetime.datetime.now()
        super().save(**kwargs)


class FuncPosition(BaseModel):
    title = CharField(verbose_name='Должность')

    def __str__(self):
        return self.title


class Person(BaseModel):
    surname = CharField(verbose_name='Фамилия')
    name = CharField(verbose_name='Имя')
    second_name = CharField(null=True, verbose_name='Отчество')
    table_num = CharField(unique=True, verbose_name='Табельный номер')
    function = ForeignKeyField(FuncPosition, verbose_name='Должность', on_delete='CASCADE')

    def __str__(self):
        return f'{self.surname} {self.name[:1]}.{self.second_name[:1]}. ({self.function})'


class Status(BaseModel):
    state = CharField(verbose_name='Наименование')

    def __str__(self):
        return self.state


class WorkTask(BaseModel):
    type_obj = CharField(verbose_name='Тип объекта')
    title = CharField(verbose_name='Наименование объекта')
    article = CharField(verbose_name='Конструктив')
    order = CharField(verbose_name='Производственный заказ')
    deadline = SmallIntegerField(verbose_name='Норматив выполнения')
    master = ForeignKeyField(Person, backref='tasks', verbose_name='Работник', on_delete='CASCADE')
    status = ForeignKeyField(Status, backref='tasks', verbose_name='Состояние', default=1, on_delete='CASCADE')
    comment = TextField(verbose_name='Комментарий', null=True)

    def __str__(self):
        return self.order


class WorkLapse(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='time_worked', on_delete='CASCADE')
    task = ForeignKeyField(WorkTask, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    date = DateField(default=datetime.datetime.now, verbose_name='Дата')
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.value} ч. ({self.date:%d-%m-%Y})'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented


class Turn(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='turns', on_delete='CASCADE')
    date = DateField(verbose_name='Дата', default=datetime.datetime.now)
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.value} ч.'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented


# from database.models import *
# with get_database().atomic():
#     FuncPosition.insert_many([['Монтажник'], ['Слесарь']], fields=['title']).execute()
#     Status.insert_many([['В работе'], ['Завершен'], ['Приостановлен']], ['state']).execute()
#     data_person = [
#         {'surname': 'Вахитов', 'name': 'Данис', 'second_name': 'Римович', 'table_num': '1', 'function': 1},
#         {'surname': 'Найденко', 'name': 'Георгий', 'second_name': 'Владимирович', 'table_num': '2', 'function': 1},
#         {'surname': 'Шмырин', 'name': 'Олег', 'second_name': 'Афанасьевич', 'table_num': '3', 'function': 1},
#         {'surname': 'Прокопенко', 'name': 'Юрий', 'second_name': 'Валерьевич', 'table_num': '4', 'function': 1},
#         {'surname': 'Полякова', 'name': 'Мирина', 'second_name': 'Ивановна', 'table_num': '5', 'function': 1},
#         {'surname': 'Коробка', 'name': 'Алексей', 'second_name': 'Викторович', 'table_num': '6', 'function': 2},
#         {'surname': 'Пузанков', 'name': 'Максим', 'second_name': 'Витальевич', 'table_num': '7', 'function': 2},
#         {'surname': 'Аскеров', 'name': 'Гахраман', 'second_name': 'Камаладдин Оглы', 'table_num': '8', 'function': 2},
#     ]
#     Person.insert_many(data_person).execute()
#     data_task = [
#         {'type_obj': 'Ру-10кВ', 'title': 'Ярино', 'article': 'ENF10_637_03_044_00', 'order': 'ПР-028108', 'deadline': 42, 'master': 1},
#         {'type_obj': 'Ру-10кВ ЛЭП АБ', 'title': 'Ярино', 'article': 'ENF10_633_00_000_00-65', 'order': 'ПР-028208', 'deadline': 24, 'master': 2},
#         {'type_obj': 'Ру-10кВ', 'title': 'Абакумовка', 'article': 'ENF10_633_00_000_00-65', 'order': 'ПР-028258', 'deadline': 24, 'master': 3},
#         {'type_obj': 'Ру-10кВ ЛЭП АБ', 'title': 'Ярино', 'article': 'ENF10_633_00_000_00-65', 'order': 'ПР-028278', 'deadline': 24, 'master': 4},
#         {'type_obj': 'Ру-20кВ', 'title': 'ЗИЛ', 'article': 'ENF20_003_00_000_00-03', 'order': 'ПР-028103', 'deadline': 24, 'master': 5},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_003_00_000_00-03', 'order': 'ПР-028203', 'deadline': 24, 'master': 1},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_634_03_022_00', 'order': 'ПР-027111', 'deadline': 42, 'master': 2},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_635_00_000_00-03', 'order': 'ПР-028643', 'deadline': 24, 'master': 3},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028104', 'deadline': 24, 'master': 4},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028113', 'deadline': 24, 'master': 5},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028313', 'deadline': 54, 'master': 6},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028313', 'deadline': 54, 'master': 7},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028313', 'deadline': 54, 'master': 8},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028314', 'deadline': 54, 'master': 6},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028314', 'deadline': 54, 'master': 7},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028314', 'deadline': 54, 'master': 8},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028315', 'deadline': 54, 'master': 6},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028315', 'deadline': 54, 'master': 7},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028315', 'deadline': 54, 'master': 8},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028316', 'deadline': 54, 'master': 6},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028316', 'deadline': 54, 'master': 7},
#         {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028316', 'deadline': 54, 'master': 8},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028317', 'deadline': 54, 'master': 6},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028317', 'deadline': 54, 'master': 7},
#         {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028317', 'deadline': 54, 'master': 8},
#     ]
#     WorkTask.insert_many(data_task).execute()
#
#     # import datetime
#     import random
#     target_date = datetime.date(2024, 7, 11)
#     work_lapse_data = []
#     for _ in range(50):
#         for worker in Person.select():
#             print(f'{worker}')
#             if random.random() > 0.05:
#                 print("сработало")
#                 task = random.choice(worker.tasks)
#                 duration = random.choice([8, 12])
#                 print(f'{task=} {duration=}')
#                 if sum(task.time_worked) < 1.1 * task.deadline:
#                     laps = {'worker': worker, 'task': task, 'value': duration, 'date': target_date}
#                     WorkLapse.create(**laps)
#                     work_lapse_data.append(laps)
#         target_date += datetime.timedelta(days=1)
#     # for i in range(0, len(work_lapse_data), 50):
#     #     WorkLapse.insert_many(work_lapse_data[i:i + 50]).execute()



# tasks = WorkTask.select(WorkTask.id, WorkTask.order, WorkTask.duration, fn.SUM(WorkLapse.term).alias('total')).join(WorkLapse, JOIN.LEFT_OUTER).group_by(WorkTask.id).dicts()
# tasks = WorkTask.select(WorkTask, Status).join(Status)
# laps = WorkLapse.select()
# result = prefetch(tasks, laps)
#
# ts = WorkTask.select(WorkTask.order, WorkTask.duration, WorkTask.time_worked, fn.SUM(WorkTask.time_worked).alias('summ'))
