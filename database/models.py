from datetime import datetime

from peewee import *

from .utils import get_database


class BaseModel(Model):
    create_at = DateTimeField(default=datetime.now, verbose_name='Дата создания')
    update_at = DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    class Meta:
        database = get_database()
        only_save_dirty = True

    def save(self, **kwargs):
        self.update_at = datetime.now()
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
    equipment = CharField(verbose_name='Тип объекта')
    title = CharField(verbose_name='Наименование объекта')
    article = CharField(verbose_name='Конструктив')
    order = CharField(verbose_name='Производственный заказ')
    deadline = SmallIntegerField(verbose_name='Норматив выполнения')
    master = ForeignKeyField(Person, backref='tasks', verbose_name='Работник', on_delete='CASCADE')
    status = ForeignKeyField(Status, backref='tasks', verbose_name='Состояние', default=1, on_delete='CASCADE')
    duration = SmallIntegerField(verbose_name="Общая продолжительность", default=0)
    comment = TextField(verbose_name='Комментарий', null=True)

    def __str__(self):
        # return f'{self.order} ({self.status})'
        return self.order


class WorkLapse(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='time_worked', on_delete='CASCADE')
    task = ForeignKeyField(WorkTask, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    term = SmallIntegerField(verbose_name="Продолжительность")
    date = DateField(default=datetime.now, verbose_name='Дата')

    def __str__(self):
        return f'{self.term} ч. ({self.date:%d-%m-%Y})'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.term + other.term) if isinstance(other, self.__class__) else (
            int(self.term + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.term) if isinstance(other, (int, float)) else NotImplemented

    def save(self, **kwargs):
        super().save(**kwargs)
        self.task.duration = sum(self.task.time_worked)
        self.task.save()


class Turn(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='turns', on_delete='CASCADE')
    date = DateField(verbose_name='Дата', default=datetime.now)
    duration = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.duration} ч.'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.duration + other.duration) if isinstance(other, self.__class__) else (
            int(self.duration + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.duration) if isinstance(other, (int, float)) else NotImplemented


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
#         {'equipment': 'Ру10кВ', 'title': 'Ярино', 'article': 'ENF10_637_03_044_00', 'order': 'ПР-028108', 'deadline': 42, 'master': 1},
#         {'equipment': 'Ру10кВ ЛЭП АБ', 'title': 'Ярино', 'article': 'ENF10_633_00_000_00-65', 'order': 'ПР-028208', 'deadline': 24, 'master': 2},
#         {'equipment': 'Ру10кВ', 'title': 'Абакумовка', 'article': 'ENF10_633_00_000_00-65', 'order': 'ПР-028258', 'deadline': 24, 'master': 3},
#         {'equipment': 'Ру10кВ ЛЭП АБ', 'title': 'Ярино', 'article': 'ENF10_633_00_000_00-65', 'order': 'ПР-028278', 'deadline': 24, 'master': 4},
#         {'equipment': 'Ру20кВ', 'title': 'ЗИЛ', 'article': 'ENF20_003_00_000_00-03', 'order': 'ПР-028103', 'deadline': 24, 'master': 5},
#         {'equipment': 'Ру10кВ', 'title': 'Саларьево', 'article': 'ENF10_003_00_000_00-03', 'order': 'ПР-028103', 'deadline': 24, 'master': 1},
#         {'equipment': 'Ру10кВ', 'title': 'Саянская', 'article': 'ENF10_634_03_022_00', 'order': 'ПР-027111', 'deadline': 42, 'master': 2},
#         {'equipment': 'Ру10кВ', 'title': 'Саларьево', 'article': 'ENF10_635_00_000_00-03', 'order': 'ПР-028643', 'deadline': 24, 'master': 3},
#         {'equipment': 'Ру10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028104', 'deadline': 24, 'master': 4},
#         {'equipment': 'Ру10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028113', 'deadline': 24, 'master': 5},
#         {'equipment': 'Ру10кВ', 'title': 'Ванино', 'article': '633-67 - 2 шт 629-18 - 2шт', 'order': 'сборка', 'deadline': 54 * 4 // 3, 'master': 6},
#         {'equipment': 'Ру10кВ', 'title': 'Ванино', 'article': '633-67 - 2 шт 629-18 - 2шт', 'order': 'сборка', 'deadline': 54 * 4 // 3, 'master': 7},
#         {'equipment': 'Ру10кВ', 'title': 'Ванино', 'article': '633-67 - 2 шт 629-18 - 2шт', 'order': 'сборка', 'deadline': 54 * 4 // 3, 'master': 8},
#         {'equipment': 'Ру10кВ', 'title': 'Саларьево', 'article': '630-33 - 2шт 632-10 - 1шт', 'order': 'сборка', 'deadline': 54, 'master': 6},
#         {'equipment': 'Ру10кВ', 'title': 'Саларьево', 'article': '630-33 - 2шт 632-10 - 1шт', 'order': 'сборка', 'deadline': 54, 'master': 7},
#         {'equipment': 'Ру10кВ', 'title': 'Саларьево', 'article': '630-33 - 2шт 632-10 - 1шт', 'order': 'сборка', 'deadline': 54, 'master': 8},
#         {'equipment': 'Ру10кВ', 'title': 'Саянская', 'article': '637-40 - 2шт 638-11 - 2шт', 'order': 'сборка', 'deadline': 54 * 4 // 3, 'master': 6},
#         {'equipment': 'Ру10кВ', 'title': 'Саянская', 'article': '637-40 - 2шт 638-11 - 2шт', 'order': 'сборка', 'deadline': 54 * 4 // 3, 'master': 7},
#         {'equipment': 'Ру10кВ', 'title': 'Саянская', 'article': '637-40 - 2шт 638-11 - 2шт', 'order': 'сборка', 'deadline': 54 * 4 // 3, 'master': 7},
#     ]
#     WorkTask.insert_many(data_task).execute()
#     work_lapse_data = []
#     import random
#     for _ in range(50):
#         task = random.randint(1, 19)
#         term = random.randint(1, 12)
#         month = random.randint(1, 12)
#         day = random.randint(1, 15)
#         laps = {'worker': WorkTask[task].master, 'task': WorkTask[task], 'term': term, 'date': f'2024-{month}-{day}'}
#         WorkLapse.create(**laps)
        # work_lapse_data.append(laps)
    # WorkLapse.insert_many(work_lapse_data).execute()

# tasks = WorkTask.select(WorkTask.order, WorkTask.duration, fn.SUM(WorkLapse.term).alias('summ')).join(WorkLapse, JOIN.LEFT_OUTER)
# tasks = WorkTask.select(WorkTask, Status).join(Status)
# laps = WorkLapse.select()
# result = prefetch(tasks, laps)

# ts = WorkTask.select(WorkTask.order, WorkTask.duration, WorkTask.time_worked, fn.SUM(WorkTask.time_worked).alias('summ'))
