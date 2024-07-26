from datetime import datetime

from peewee import *

from .utils import get_database


class BaseModel(Model):
    class Meta:
        database = get_database()
        only_save_dirty = True


class FuncPosition(BaseModel):
    title = CharField(verbose_name='Должность')

    def __str__(self):
        return self.title


class Person(BaseModel):
    surname = CharField(verbose_name='Фамилия')
    name = CharField(verbose_name='Имя')
    second_name = CharField(null=True, verbose_name='Отчество')
    table_num = CharField(unique=True, verbose_name='Табельный номер')
    function = ForeignKeyField(FuncPosition, verbose_name='Должность')

    def __str__(self):
        return f'{self.surname} {self.name[:1]}.{self.second_name[:1]}. ({self.function})'


class WorkTask(BaseModel):
    equipment = CharField(verbose_name='Тип объекта')
    title = CharField(verbose_name='Наименование объекта')
    article = CharField(verbose_name='Конструктив')
    order = CharField(verbose_name='Производственный заказ')
    deadline = SmallIntegerField(verbose_name='Норматив выполнения')
    master = ForeignKeyField(Person, backref='tasks', verbose_name='Работник')
    status = BooleanField(verbose_name='Состояние', default=True)
    duration = SmallIntegerField(verbose_name="Общая продолжительность", default=0)

    def __str__(self):
        return f'{self.order} ({"в работе" if self.status else "завершен"})'

    @property
    def get_status(self):
        return f'{"в работе" if self.status else "завершен"}'

    @get_status.setter
    def get_status(self, status):
        self.status = status


class WorkLapse(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='time_worked')
    task = ForeignKeyField(WorkTask, backref='time_worked', verbose_name='Задача')
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
        self.task.duration += self.term
        self.task.save()


class Turn(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='turns')
    date = DateField(verbose_name='Дата', default=datetime.now())
    duration = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.duration} ч.'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.duration + other.duration) if isinstance(other, self.__class__) else (
            int(self.duration + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.duration) if isinstance(other, (int, float)) else NotImplemented


# from database.models import *
# mont = FuncPosition.create(title='Монтажник')
# sles = FuncPosition.create(title='Слесарь')
# vaxa = Person.create(surname='Вахитов', name='Данис', second_name='Римович', table_num='1', function=mont)
# naid = Person.create(surname='Найденко', name='Георгий', second_name='Владимирович', table_num='2', function=mont)
# shmir = Person.create(surname='Шмырин', name='Олег', second_name='Афанасьевич', table_num='3', function=mont)
# prokop = Person.create(surname='Прокопенко', name='Юрий', second_name='Валерьевич', table_num='4', function=mont)
# poly = Person.create(surname='Полякова', name='Мирина', second_name='Ивановна', table_num='5', function=mont)
# korob = Person.create(surname='Коробка', name='Алексей', second_name='Викторович', table_num='6', function=sles)
# puza = Person.create(surname='Пузанков', name='Максим', second_name='Витальевич', table_num='7', function=sles)
# ask = Person.create(surname='Аскеров', name='Гахраман', second_name='Камаладдин Оглы', table_num='8', function=sles)
# task1 = WorkTask.create(equipment='Ру10кВ', title='Ярино', article='ENF10_637_03_044_00', order='ПР-028108', deadline=42, master=vaxa)
# task2 = WorkTask.create(equipment='Ру10кВ ЛЭП АБ', title='Ярино', article='ENF10_633_00_000_00-65', order='ПР-028208', deadline=24, master=naid)
# task3 = WorkTask.create(equipment='Ру10кВ', title='Абакумовка', article='ENF10_633_00_000_00-65', order='ПР-028208', deadline=24, master=prokop)
# task4 = WorkTask.create(equipment='Ру10кВ ЛЭП АБ', title='Ярино', article='ENF10_633_00_000_00-65', order='ПР-028208', deadline=24, master=vaxa)
# task5 = WorkTask.create(equipment='Ру20кВ', title='ЗИЛ', article='ENF20_003_00_000_00-03', order='ПР-028103', deadline=24, master=poly)
# task6 = WorkTask.create(equipment='Ру10кВ', title='Саларьево', article='ENF10_003_00_000_00-03', order='ПР-028103', deadline=24, master=shmir)
# task7 = WorkTask.create(equipment='Ру10кВ', title='Саянская', article='ENF10_634_03_022_00', order='ПР-027111', deadline=42, master=naid)
# task8 = WorkTask.create(equipment='Ру10кВ', title='Саларьево', article='ENF10_635_00_000_00-03', order='ПР-028643', deadline=24, master=prokop)
# task9 = WorkTask.create(equipment='Ру10кВ', title='Ванино', article='ENF10_629_00_000_00-18', order='ПР-028104', deadline=24, master=poly)
# task0 = WorkTask.create(equipment='Ру10кВ', title='Ванино', article='ENF10_633_00_000_00-67', order='ПР-028113', deadline=24, master=prokop)
# task10 = WorkTask.create(equipment='Ру10кВ', title='Ванино', article='633-67 - 2 шт 629-18 - 2шт', order='сборка', deadline=54 * 4 // 3, master=korob)
# task11 = WorkTask.create(equipment='Ру10кВ', title='Ванино', article='633-67 - 2 шт 629-18 - 2шт', order='сборка', deadline=54 * 4 // 3, master=puza)
# task12 = WorkTask.create(equipment='Ру10кВ', title='Ванино', article='633-67 - 2 шт 629-18 - 2шт', order='сборка', deadline=54 * 4 // 3, master=ask)
# task20 = WorkTask.create(equipment='Ру10кВ', title='Саларьево', article='630-33 - 2шт 632-10 - 1шт', order='сборка', deadline=54, master=korob)
# task21 = WorkTask.create(equipment='Ру10кВ', title='Саларьево', article='630-33 - 2шт 632-10 - 1шт', order='сборка', deadline=54, master=puza)
# task22 = WorkTask.create(equipment='Ру10кВ', title='Саларьево', article='630-33 - 2шт 632-10 - 1шт', order='сборка', deadline=54, master=ask)
# task30 = WorkTask.create(equipment='Ру10кВ', title='Саянская', article='637-40 - 2шт 638-11 - 2шт', order='сборка', deadline=54 * 4 // 3, master=korob)
# task31 = WorkTask.create(equipment='Ру10кВ', title='Саянская', article='637-40 - 2шт 638-11 - 2шт', order='сборка', deadline=54 * 4 // 3, master=puza)
# task32 = WorkTask.create(equipment='Ру10кВ', title='Саянская', article='637-40 - 2шт 638-11 - 2шт', order='сборка', deadline=54 * 4 // 3, master=ask)
# import random
# for _ in range(50):
#     task = random.choice([task1, task2, task3, task4, task5, task6, task7, task8, task9, task0, task10, task11, task12, task20, task21, task22, task30, task31, task32])
#     term = random.randint(1, 12)
#     month = random.randint(1, 12)
#     day = random.randint(1, 15)
#     WorkLapse.create(worker=task.master, task=task, term=term, date=f'2024-{month}-{day}')
